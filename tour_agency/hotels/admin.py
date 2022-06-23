from django.contrib import admin

from hotels.models import Hotel, Room, RoomReservation, RoomType, Convenience


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
                    "square",
                    "is_family",
                    "description",
                    "conveniences",
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
