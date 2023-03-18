from django.contrib import admin
from .models import Category, Event

# einfachste Möglichkeit, ein Model in der Admin zu registrieren
#  admin.site.register(Category)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    # zeigt die Attribute in der Übersicht an
    list_display = ["id", "name", "sub_title", "number_of_events"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "sub_title", "description"]

    def number_of_events(self, obj):
        # für jedes Objekt in der Ausgabemenge via dem related Manager
        # events die count-Methode aufrufen
        return obj.events.count()


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id",
                    "name",
                    "sub_title",
                    "author",
                    "category",
                    "is_active"
                    ]
    list_display_links = ["id", "name"]
    search_fields = ["name", "sub_title", "description"]
    actions = ["make_active", "make_inactive"]
    readonly_fields = ["author"]  # ist nicht änderbar

    @admin.display(description="setze ausgewählte aktiv")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.display(description="setze ausgewählte inaktiv")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    def get_queryset(self, request):
        """ 
        Queryset überschreiben: Kann nur die Einträge sehen,
        die ich (request.user) erstellt habe. bzw. mir gehören
        """
        return super().get_queryset(request)
        # qs = super().get_queryset(request)
        # return qs.filter(author=request.user)
