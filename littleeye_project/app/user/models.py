from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    TUTOR = "TUTOR", "Tutor"
    STUDENT = "STUDENT", "Student"


class User(AbstractUser):
    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)

    # def save(self, *args, **kwargs):
    # if not self.pk:
    # self.role = self.base_role
    # return super().save(*args, **kwargs)
