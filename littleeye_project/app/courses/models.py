from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    lecturer = models.ManyToManyField(
        User, related_name="courses", limit_choices_to={"role": "TUTOR"}
    )

    def __str__(self):
        return self.name
