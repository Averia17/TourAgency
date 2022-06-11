from django.contrib import admin

from locations.models import Country, City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {"fields": ["name"]},
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "country"]
    list_filter = ["country"]
    search_fields = ["name"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {"fields": ["name", "country"]},
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
