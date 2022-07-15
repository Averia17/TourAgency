from django.contrib import admin

from images.admin import save_related_images, ImageInline
from images.models import MultiCityTourImage, OneCityTourImage
from tours.models import (
    MultiCityTour,
    OneCityTour,
    TourFeature,
    MultiCityArrivalDate,
    OneCityArrivalDate,
)


class MultiCityTourImageInline(ImageInline):
    model = MultiCityTourImage


class OneCityTourImageInline(ImageInline):
    model = OneCityTourImage


class MultiCityArrivalDateInline(admin.TabularInline):
    model = MultiCityArrivalDate
    extra = 1


class OneCityArrivalDateInline(admin.TabularInline):
    model = OneCityArrivalDate
    extra = 1


@admin.register(MultiCityTour)
class MultiCityTourAdmin(admin.ModelAdmin):
    inlines = [MultiCityTourImageInline, MultiCityArrivalDateInline]
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
                    "price",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
    related_field = "tour"

    def save_formset(self, request, form, formset, change, **kwargs):
        if formset.model != MultiCityTourImage:
            return super().save_formset(request, form, formset, change)
        save_related_images(request, form, formset, self.related_field)


@admin.register(OneCityTour)
class OneCityTourAdmin(admin.ModelAdmin):
    inlines = [OneCityTourImageInline, OneCityArrivalDateInline]
    list_display = ["title"]
    list_filter = ["destination"]
    search_fields = ["title"]
    readonly_fields = ["nights", "created", "modified"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "description",
                    "destination",
                    "hotel",
                    "days",
                    "nights",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
    related_field = "tour"

    def save_formset(self, request, form, formset, change, **kwargs):
        if formset.model != OneCityTourImage:
            return super().save_formset(request, form, formset, change)
        save_related_images(request, form, formset, self.related_field)


@admin.register(TourFeature)
class TourFeatureAdmin(admin.ModelAdmin):
    list_display = ["title", "tour", "day", "destination"]
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
                    "day",
                    "destination",
                    "hotel",
                    "food",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
