from rest_framework.fields import ListField, ImageField
from rest_framework.serializers import ModelSerializer

from images.models import Image
from images.services import FileStandardUploadService


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ("url",)

    def to_representation(self, instance):
        return super().to_representation(instance).get("url")


class ImageUploadSerializer(ModelSerializer):
    uploaded_images = ListField(child=ImageField(), write_only=True, required=False)

    image_model = Image
    additional_field = ""

    class Meta:
        fields = ("uploaded_images",)

    def create(self, validated_data):
        images = validated_data.pop("uploaded_images", [])
        instance = super().create(validated_data)
        user = self.context["request"].user
        service = FileStandardUploadService(self.image_model, user)
        for image in images:
            service.create(image, {self.additional_field: instance})
        return instance

    def update(self, instance, validated_data):
        images = validated_data.pop("uploaded_images", None)
        instance = super().update(instance, validated_data)
        user = self.context["request"].user
        if images is not None:
            instance.images.clear()
            service = FileStandardUploadService(self.image_model, user)
            for image in images:
                service.create(image, {self.additional_field: instance})
        return instance
