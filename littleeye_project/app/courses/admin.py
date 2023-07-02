from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ["name", "tutor"]
    list_display = ("name", "tutor")
