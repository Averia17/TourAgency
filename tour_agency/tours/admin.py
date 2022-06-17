from django.contrib import admin

from tours.models import MultiCityTour, TourFeature


@admin.register(MultiCityTour)
class MultiCityTourAdmin(admin.ModelAdmin):
    list_display = ["title", "tour_type", "price"]
    list_filter = ["tour_type"]
    search_fields = ["title"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "description",
                    "tour_type",
                    "start",
                    "end",
                    "price",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]


@admin.register(TourFeature)
class TourFeatureAdmin(admin.ModelAdmin):
    list_display = ["title", "tour", "day", "city"]
    list_filter = ["city"]
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
                    "city",
                    "hotel",
                    "food",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
