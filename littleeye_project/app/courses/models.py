from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    name = models.CharField(max_length=200)
    shortcut = models.CharField(max_length=20)
    tutor = models.ForeignKey(
        User,
        related_name="courses",
        on_delete=models.CASCADE,
        limit_choices_to={"role": "TUTOR"},
    )

    def __str__(self):
        return self.name
