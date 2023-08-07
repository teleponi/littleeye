from django.contrib import admin
from .models import Ticket, MediaType, Tag, TicketHistory, Comment


class CommentInlineAdmin(admin.TabularInline):
    model = Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(TicketHistory)
class Historyadmin(admin.ModelAdmin):
    search_fields = ["ticket"]
    list_display = ("ticket", "updated_by", "type", "created_at")
    list_filter = ("ticket",)
    readonly_fields = (
        "type",
        "ticket",
        "comment",
        "updated_by",
        "severity",
        "status",
        "address_report",
    )

    @admin.display(description="Kommentar")
    def address_report(self, instance):
        return instance.comment.description


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
    inlines = [CommentInlineAdmin]
    search_fields = ["name"]
    list_display = "name", "course", "severity", "author", "course_tutor"

    def course_tutor(self, obj):
        return obj.course.tutor
