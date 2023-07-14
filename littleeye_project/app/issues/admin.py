from django.contrib import admin
from .models import Issue, MediaType, Tag, IssueHistory


@admin.register(IssueHistory)
class Historyadmin(admin.ModelAdmin):
    search_fields = ["issue"]
    list_display = ("issue", "type", "created_at")
    list_filter = ("issue",)


@admin.register(Tag)
class Tagdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name",)


@admin.register(MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name",)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = "name", "course", "severity", "author", "course_tutor"

    def course_tutor(self, obj):
        return obj.course.tutor
