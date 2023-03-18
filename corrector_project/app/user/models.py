from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """unser Model erbt von Abstract User."""

    address = models.CharField(max_length=250, blank=True, null=True)

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MODERATOR = "MODERATOR", "Moderator"
        PREMIUM = "PREMIUM", "Premium User"

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)
