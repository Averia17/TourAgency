from django.contrib import admin

from images.admin import save_related_images, ImageInline
from images.models import TourImage
from tours.arrival_dates.admin import ArrivalDateInline
from tours.models import Tour, TourFeature


class TourImageInline(ImageInline):
    model = TourImage


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    inlines = [TourImageInline, ArrivalDateInline]
    list_display = ["title", "tour_type", "price"]
    list_filter = ["tour_type"]
    search_fields = ["title"]
    readonly_fields = ["days", "created", "modified"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "description",
                    "days",
                    "tour_type",
                    "max_passengers",
                    "price",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
    related_field = "tour"

    def save_formset(self, request, form, formset, change, **kwargs):
        if formset.model != TourImage:
            return super().save_formset(request, form, formset, change)
        save_related_images(request, form, formset, self.related_field)


@admin.register(TourFeature)
class TourFeatureAdmin(admin.ModelAdmin):
    list_display = ["title", "tour", "days", "destination"]
    list_filter = ["destination"]
    search_fields = ["title"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "description",
                    "tour",
                    "days",
                    "destination",
                    "hotel",
                    "food",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
