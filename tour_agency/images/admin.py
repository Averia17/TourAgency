from collections import OrderedDict

from django.contrib import admin, messages
from django import forms
from django.core.exceptions import ValidationError
from images.services import FileStandardUploadService
from images.models import Image, HotelImage, RoomImage, TourImage


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "original_file_name",
        "file_name",
        "file_type",
        "url",
        "uploaded_by",
    ]
    additional_fields = []

    def get_fields(self, request, obj=None):
        return list(
            OrderedDict.fromkeys(
                self.additional_fields
                + super(ImageAdmin, self).get_fields(request, obj)
            )
        )

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.form = ImageForm

        return super().get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ["created", "modified"]

        if obj is not None:
            return readonly_fields + [
                "original_file_name",
                "file_name",
                "file_type",
            ]

        return readonly_fields

    def save_model(self, request, obj, form, change, **kwargs):
        try:
            cleaned_data = form.cleaned_data

            service = FileStandardUploadService(
                self.model, request.user, cleaned_data["image"]
            )
            for field in self.additional_fields:
                kwargs[field] = cleaned_data.get(field)
            if change:
                service.update(file=obj, **kwargs)
            else:
                service.create(**kwargs)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)

    # disable editing
    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj=obj) if not obj else False


@admin.register(HotelImage)
class HotelImageAdmin(ImageAdmin):
    additional_fields = ["hotel"]


@admin.register(RoomImage)
class RoomImageAdmin(ImageAdmin):
    additional_form_fields = ["room"]


@admin.register(TourImage)
class RoomImageAdmin(ImageAdmin):
    additional_form_fields = ["tour"]
