from dataclasses import fields

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Branch
from .models import AccessibilityForm

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Şube Bilgisi", {"fields": ("branch",)}),
    )

    list_display = UserAdmin.list_display + ('branch',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Branch)
admin.site.register(AccessibilityForm)