from rest_framework.fields import CharField, SerializerMethodField, ListField, ImageField
from rest_framework.serializers import ModelSerializer

from core.utils import string_to_datetime
from hotels.models import Hotel, RoomType, Convenience
from images.models import HotelImage
from images.serializers import ImageSerializer, ImageUploadSerializer
from images.services import FileStandardUploadService
from locations.serializers import CitySerializer
from tours.services import AvailableRoomsService


class ConvenienceSerializer(ModelSerializer):
    icon = CharField(source="icon.url")

    class Meta:
        model = Convenience
        fields = ("name", "icon")


class RoomTypeSerializer(ModelSerializer):
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = RoomType
        fields = (
            "id",
            "name",
            "cost_per_day",
            "count_places",
            "is_family",
            "conveniences",
            "images",
            "description",
        )

    def to_representation(self, instance):
        self.fields["conveniences"] = ConvenienceSerializer(many=True)
        result = super().to_representation(instance)
        request = self.context.get("request")
        start_date = request.query_params.get("start", None) if request else None
        end_date = request.query_params.get("end", None) if request else None
        if start_date and end_date:
            result["is_available"] = instance.is_available(
                string_to_datetime(start_date), string_to_datetime(end_date)
            )
        return result


class RoomDetailSerializer(RoomTypeSerializer):
    class Meta(RoomTypeSerializer.Meta):
        fields = RoomTypeSerializer.Meta.fields + (
            "square",
            "is_family",
            "description",
        )


class RoomCreateSerializer(ModelSerializer):
    class Meta:
        model = RoomType
        fields = "__all__"


# TODO: search better way to create serializer with {id: "", name: ""}
class SimpleHotelSerializer(ModelSerializer):
    image = ImageSerializer(source="images", many=True)

    class Meta:
        model = Hotel
        fields = ("id", "name", "image")

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.update({"image": result["image"][0] if result["image"] else None})
        return result


class HotelSerializer(ImageUploadSerializer):
    images = ImageSerializer(many=True, read_only=True)

    image_model = HotelImage
    additional_field = "hotel"

    class Meta:
        model = Hotel
        fields = (
            "id",
            "name",
            "stars_number",
            "city",
            "street",
            "images",
        )

    def to_representation(self, instance):
        self.fields["city"] = CitySerializer(read_only=True)
        return super().to_representation(instance)


class HotelDetailSerializer(HotelSerializer):
    room_types = SerializerMethodField()

    class Meta(HotelSerializer.Meta):
        fields = HotelSerializer.Meta.fields + (
            "room_types",
            "description",
        )

    def get_room_types(self, obj):
        start = self.context.get("start")
        end = self.context.get("end")
        rooms = AvailableRoomsService(
            self.context.get("filter_params"),
        ).get_rooms(obj, start, end)
        return RoomTypeSerializer(rooms, many=True).data
