from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', _('Admin')),
        ('user', _('User')),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    two_factor_enabled = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"