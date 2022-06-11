from rest_framework.serializers import ModelSerializer

from hotels.models import Hotel, RoomType
from locations.serializers import CitySerializer


class RoomTypeSerializer(ModelSerializer):
    class Meta:
        model = RoomType
        fields = ("id", "name", "cost_per_day", "count_places")


class RoomTypeDetailSerializer(RoomTypeSerializer):
    class Meta(RoomTypeSerializer.Meta):
        fields = RoomTypeSerializer.Meta.fields + (
            "square",
            "is_family",
            "has_balcony",
            "description",
        )


class HotelSerializer(ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Hotel
        fields = ("id", "name", "stars_number", "city", "image_url")


class HotelDetailSerializer(HotelSerializer):
    room_types = RoomTypeSerializer(many=True)

    class Meta(HotelSerializer.Meta):
        fields = HotelSerializer.Meta.fields + ("room_types", "street", "description")
