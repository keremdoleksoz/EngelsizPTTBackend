from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Branch model
class Branch(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# User model
class CustomUser(AbstractUser):
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.branch})"


ACCESSIBILITY_CHOICES = [
    ('yes', 'Evet, yeterli'),
    ('no', 'Hayır, yok'),
    ('partial', 'Var ama yetersiz'),
]

# Accessibility Form
class AccessibilityForm(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    has_ramp = models.CharField(
        max_length=10,
        choices=ACCESSIBILITY_CHOICES,
        verbose_name="Engelli Rampası"
    )

    has_wheelchair_access = models.CharField(
        max_length=10,
        choices=ACCESSIBILITY_CHOICES,
        verbose_name="Tekerlekli sandalye erişimi"
    )

    has_disable_parking = models.CharField(
        max_length=10,
        choices=ACCESSIBILITY_CHOICES,
        verbose_name="Engelli Otoparkı"
    )

    has_automatic_door = models.CharField(
        max_length=10,
        choices=ACCESSIBILITY_CHOICES,
        verbose_name="Otomatik Kapı"
    )

    has_personel_support_visual = models.CharField(
        max_length=10,
        choices=ACCESSIBILITY_CHOICES,
        verbose_name="Eğitimli Personel Desteği"
    )

    has_braille_signs = models.CharField(
        max_length=10,
        choices=ACCESSIBILITY_CHOICES,
        verbose_name="Braille Tabelaları"
    )

    has_audio_guidance = models.CharField(
        max_length=10,
        choices=ACCESSIBILITY_CHOICES,
        verbose_name="Sesli yönlendirme sistemi"
    )

    has_audio_guidance_atm = models.CharField(
        max_length=10,
        choices=ACCESSIBILITY_CHOICES,
        verbose_name="ATM'lerde Sesli Yönlendirme"
    )

    has_personel_support_hearing = models.CharField(
        max_length=10,
        choices=ACCESSIBILITY_CHOICES,
        verbose_name="Eğitimli Personel Desteği "
    )

    has_personel_support_physical = models.CharField(
        max_length=10,
        choices=ACCESSIBILITY_CHOICES,
        verbose_name="Eğitimli Personel Desteği"
    )

    has_visual_guide = models.CharField(
        max_length=10,
        choices=ACCESSIBILITY_CHOICES,
        verbose_name="Görsel Yönlendirme Sistemi"
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.branch.name} - Erişilebilirlik Formu"
