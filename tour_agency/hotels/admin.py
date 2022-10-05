from django.contrib import admin

from hotels.models import Hotel, RoomType, Convenience
from images.admin import save_related_images, ImageInline
from images.models import HotelImage, RoomImage


class HotelImageInline(ImageInline):
    model = HotelImage


class RoomImageInline(ImageInline):
    model = RoomImage


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageInline]
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
    related_field = "hotel"

    def save_formset(self, request, form, formset, change, **kwargs):
        if formset.model != HotelImage:
            return super().save_formset(request, form, formset, change)
        save_related_images(request, form, formset, self.related_field)

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == "conveniences":
            return db_field.remote_field.model._default_manager.filter(type="HOTEL")
        super().get_field_queryset(db, db_field, request)


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline]
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
    related_field = "room"

    def save_formset(self, request, form, formset, change, **kwargs):
        if formset.model != RoomImage:
            return super().save_formset(request, form, formset, change)
        save_related_images(request, form, formset, self.related_field)

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == "conveniences":
            return db_field.remote_field.model._default_manager.filter(type="ROOM")
        super().get_field_queryset(db, db_field, request)


@admin.register(Convenience)
class ConvenienceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "type"]
    list_filter = ["type"]
    search_fields = ["name"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {"fields": ["name", "icon", "type"]},
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
