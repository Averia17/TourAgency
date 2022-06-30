from django.contrib import admin

from hotels.models import Hotel, RoomType, Convenience, RoomReservation


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "stars_number"]
    list_filter = ["stars_number"]
    search_fields = ["name"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "stars_number",
                    "street",
                    "city",
                    "description",
                    "conveniences",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "hotel", "cost_per_day"]
    list_filter = ["hotel", "is_family"]
    search_fields = ["name"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "hotel",
                    "cost_per_day",
                    "count_places",
                    "count_rooms",
                    "square",
                    "is_family",
                    "description",
                    "conveniences",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]


@admin.register(Convenience)
class ConvenienceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "icon"]
    search_fields = ["name"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {"fields": ["name", "icon"]},
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]


@admin.register(RoomReservation)
class RoomReservationAdmin(admin.ModelAdmin):
    list_display = ["id", "room", "start", "end"]
    search_fields = ["room"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {"fields": ["room", "start", "end", "user"]},
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
