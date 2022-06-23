from rest_framework.serializers import ModelSerializer

from images.models import Image


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ("url",)

    def to_representation(self, instance):
        return super().to_representation(instance).get("url")
