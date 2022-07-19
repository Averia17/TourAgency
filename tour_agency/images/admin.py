from collections import OrderedDict

from django.contrib import admin, messages
from django import forms
from django.core.exceptions import ValidationError
from images.models import Image, HotelImage, RoomImage, CountryImage, TourImage

from images.services import FileStandardUploadService


def save_related_images(request, form, formset, related_field):
    instances = formset.save(commit=False)
    service = FileStandardUploadService(formset.model, request.user)
    for instance in instances:
        service.create(instance.image, {related_field: form.instance})
    formset.save_existing_objects()


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image"]


class ImageInline(admin.TabularInline):
    extra = 1
    form = ImageForm

    def has_change_permission(self, request, obj=None):
        return False


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

    def save_model(self, request, obj, form, change):
        try:
            cleaned_data = form.cleaned_data
            related_fields = {}
            service = FileStandardUploadService(self.model, request.user)
            for field in self.additional_fields:
                related_fields[field] = cleaned_data.get(field)
            service.create(cleaned_data["image"], related_fields)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)

    # disable editing
    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj=obj) if not obj else False


#
# @admin.register(HotelImage)
# class HotelImageAdmin(ImageAdmin):
#     additional_fields = ["hotel"]
#
#
# @admin.register(RoomImage)
# class RoomImageAdmin(ImageAdmin):
#     additional_fields = ["room"]
#
#
# @admin.register(TourImage)
# class TourAdmin(ImageAdmin):
#     additional_fields = ["tour"]
#
#
# @admin.register(CountryImage)
# class CountryImageAdmin(ImageAdmin):
#     additional_fields = ["country"]
