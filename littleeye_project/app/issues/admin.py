from django.contrib import admin
from .models import Ticket, MediaType, Tag, TicketHistory


@admin.register(TicketHistory)
class Historyadmin(admin.ModelAdmin):
    search_fields = ["ticket"]
    list_display = ("ticket", "type", "created_at")
    list_filter = ("ticket",)


@admin.register(Tag)
class Tagdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name",)


@admin.register(MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = "name", "course", "severity", "author", "course_tutor"

    def course_tutor(self, obj):
        return obj.course.tutor
