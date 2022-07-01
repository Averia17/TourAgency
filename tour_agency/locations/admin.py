from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from images.admin import save_related_images, ImageInline
from images.models import CountryImage
from locations.models import Country, City, Continent, Destination


class CountryImageInline(ImageInline):
    model = CountryImage


@admin.register(Continent)
class ContinentAdmin(admin.ModelAdmin):
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


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = [CountryImageInline]
    list_display = ["name"]
    search_fields = ["name"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {"fields": ["name", "continent"]},
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
    related_field = "tour"

    def save_formset(self, request, form, formset, change, **kwargs):
        if formset.model != CountryImage:
            return super().save_formset(request, form, formset, change)
        save_related_images(request, form, formset, self.related_field)


@admin.register(Destination)
class DestinationAdmin(GISModelAdmin):
    list_display = ["name", "country"]
    list_filter = ["country"]
    search_fields = ["name"]
    readonly_fields = ["created", "modified", "longitude", "latitude"]
    fieldsets = [
        (
            None,
            {"fields": ["name", "country", "longitude", "latitude", "location"]},
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]


admin.site.register(City, DestinationAdmin)
