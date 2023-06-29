from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name",)
