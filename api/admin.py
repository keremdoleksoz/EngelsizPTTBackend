from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.template.response import TemplateResponse

from .models import CustomUser, Branch, AccessibilityForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Şube Bilgisi", {"fields": ("branch",)}),
    )
    list_display = UserAdmin.list_display + ('branch',)


class AccessibilityFormAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'branch']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('results/', self.admin_site.admin_view(self.results_view), name='results'),
            path('results/<int:branch_id>/', self.admin_site.admin_view(self.branch_detail_view), name='results_detail'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        return self.results_view(request)

    def results_view(self, request):
        branches = Branch.objects.all()
        results = []

        for branch in branches:
            form = AccessibilityForm.objects.filter(branch=branch).order_by('-id').first()
            total_criteria = 11
            total_yes = 0

            if form:
                total_yes = sum([
                    form.has_ramp == "yes",
                    form.has_wheelchair_access == "yes",
                    form.has_disable_parking == "yes",
                    form.has_automatic_door == "yes",
                    form.has_personel_support_physical == "yes",
                    form.has_braille_signs == "yes",
                    form.has_audio_guidance == "yes",
                    form.has_audio_guidance_atm == "yes",
                    form.has_personel_support_visual == "yes",
                    form.has_personel_support_hearing == "yes",
                    form.has_visual_guide == "yes"
                ])

            score_percent = int((total_yes / total_criteria) * 100) if form else 0

            results.append({
                "branch": branch.name,
                "branch_id": branch.id,
                "form_count": 1 if form else 0,
                "score_percent": score_percent
            })

        context = dict(
            self.admin_site.each_context(request),
            results=results,
        )
        return TemplateResponse(request, "admin/results.html", context)

    def branch_detail_view(self, request, branch_id):
        branch = Branch.objects.get(id=branch_id)
        form = AccessibilityForm.objects.filter(branch=branch).order_by('-id').first()

        field_labels = {
            "has_ramp": "Engelli Rampası",
            "has_wheelchair_access": "Tekerlekli Sandalye Erişimi",
            "has_disable_parking": "Engelli Otoparkı",
            "has_automatic_door": "Otomatik Kapı",
            "has_personel_support_physical": "Eğitimli Personel (Fiziksel)",
            "has_braille_signs": "Braille Tabelalar",
            "has_audio_guidance": "Sesli Yönlendirme Sistemi",
            "has_audio_guidance_atm": "ATM Sesli Yönlendirme",
            "has_personel_support_visual": "Eğitimli Personel (Görme)",
            "has_personel_support_hearing": "Eğitimli Personel (İşitme)",
            "has_visual_guide": "Görsel Yönlendirme Sistemi",
        }

        criteria = {
            "bedensel": [
                "has_ramp",
                "has_wheelchair_access",
                "has_disable_parking",
                "has_automatic_door",
                "has_personel_support_physical",
            ],
            "görme": [
                "has_braille_signs",
                "has_audio_guidance",
                "has_audio_guidance_atm",
                "has_personel_support_visual",
            ],
            "işitsel": [
                "has_personel_support_hearing",
                "has_visual_guide",
            ]
        }

        results = {}
        if form:
            for category, fields in criteria.items():
                fulfilled = 0
                total = len(fields)
                partial_fields = {}
                missing_fields = {}

                for field in fields:
                    value = getattr(form, field)
                    if value == "yes":
                        fulfilled += 1
                    elif value == "partial":
                        partial_fields[field] = 1
                    else:
                        missing_fields[field] = 1

                results[category] = {
                    "fulfilled": fulfilled,
                    "total": total,
                    "complete": fulfilled == total,
                    "partial_fields": partial_fields,
                    "missing_fields": missing_fields,
                }

        context = dict(
            self.admin_site.each_context(request),
            branch=branch,
            results=results,
            field_labels=field_labels,
        )
        return TemplateResponse(request, "admin/branch_detail.html", context)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Branch)
admin.site.register(AccessibilityForm, AccessibilityFormAdmin)
