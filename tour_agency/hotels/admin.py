from django.contrib import admin

from hotels.models import Hotel, Room, RoomReservation, RoomType


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ["name", "stars_number", "city"]
    list_filter = ["city", "stars_number"]
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
                    "image_url",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "hotel", "cost_per_day"]
    list_filter = ["hotel", "is_family", "has_balcony"]
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
                    "square",
                    "is_family",
                    "has_balcony",
                    "description",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["number", "room_type"]
    list_filter = ["room_type"]
    search_fields = ["number"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "number",
                    "room_type",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]


@admin.register(RoomReservation)
class RoomReservationAdmin(admin.ModelAdmin):
    list_display = ["room", "start", "end"]
    list_filter = ["room", "user"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {"fields": ["room", "user", "start", "end"]},
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
