from django.contrib import admin
from .models import Issue, MediaType


@admin.register(MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name",)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = "name", "severity", "author", "is_active"


# Register your models here.
