from rest_framework.fields import CharField, SerializerMethodField, CurrentUserDefault
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from core.utils import string_to_list, string_to_datetime
from hotels.models import Hotel, RoomType, Convenience, RoomReservation
from hotels.services import filter_rooms
from images.models import HotelImage
from images.serializers import ImageSerializer
from images.services import FileStandardUploadService
from locations.serializers import CitySerializer
from users.models import User


class ConvenienceSerializer(ModelSerializer):
    icon = CharField(source="icon.url")

    class Meta:
        model = Convenience
        fields = ("name", "icon")


class RoomTypeSerializer(ModelSerializer):
    conveniences = ConvenienceSerializer(many=True)
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
        )

    def to_representation(self, instance):
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
            "has_balcony",
            "description",
        )


# TODO: search better way to create serializer with {id: "", name: ""}
class SimpleHotelSerializer(ModelSerializer):
    image = ImageSerializer(source="images.first")

    class Meta:
        model = Hotel
        fields = ("id", "name", "image")


class HotelSerializer(ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    conveniences = PrimaryKeyRelatedField(many=True, queryset=Convenience.objects.all())

    class Meta:
        model = Hotel
        fields = (
            "id",
            "name",
            "stars_number",
            "city",
            "street",
            "images",
            "conveniences",
        )

    def to_internal_value(self, data):
        if hasattr(data, "dict"):
            data = data.dict()
        data.pop("images", None)
        data["conveniences"] = string_to_list(data.get("conveniences"))
        return super().to_internal_value(data)

    def to_representation(self, instance):
        self.fields["city"] = CitySerializer(read_only=True)
        self.fields["conveniences"] = ConvenienceSerializer(many=True, read_only=True)
        return super().to_representation(instance)

    def create(self, validated_data):
        images = validated_data.pop("images")
        user = self.context["request"].user
        instance = super().create(validated_data)
        service = FileStandardUploadService(HotelImage, user)
        for image in images:
            service.create(image, hotel=instance)
        return instance

    def update(self, instance, validated_data):
        images = validated_data.pop("images", None)
        user = self.context["request"].user
        instance = super().update(instance, validated_data)
        if images is not None:
            instance.images.clear()
            service = FileStandardUploadService(HotelImage, user)
            for image in images:
                service.create(image, hotel=instance)
        return instance


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
        rooms = obj.room_types.all()
        if start and end:
            rooms = obj.available_rooms(start, end)
        filter_params = self.context.get("filter_params")
        if filter_params:
            rooms = filter_rooms(filter_params, rooms)
        return RoomTypeSerializer(rooms, many=True).data


class RoomReservationSerializer(HotelSerializer):
    user = PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=CurrentUserDefault()
    )

    class Meta:
        model = RoomReservation
        fields = ("user", "start", "end", "room")
