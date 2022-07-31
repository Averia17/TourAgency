import datetime

from django.db.models import Prefetch
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from core.constants import MEALS
from core.serializer_fields import ChoiceArrayField
from hotels.models import RoomType
from hotels.serializers import (
    SimpleHotelSerializer,
    HotelDetailSerializer,
    RoomTypeSerializer,
)
from images.serializers import ImageSerializer
from locations.serializers import DestinationSerializer
from tours.models import TourFeature, ArrivalDates, Tour
from tours.services import get_tour_available_rooms


class ArrivalDatesSerializer(ModelSerializer):
    class Meta:
        model = ArrivalDates
        fields = ("date", "discount")


class TourFeatureSerializer(ModelSerializer):
    hotel = SimpleHotelSerializer()
    destination = DestinationSerializer()
    food = ChoiceArrayField(choices=MEALS)

    class Meta:
        model = TourFeature
        fields = (
            "title",
            "description",
            "days",
            "order",
            "destination",
            "hotel",
            "food",
        )


class TourFeatureDetailSerializer(TourFeatureSerializer):
    hotel = HotelDetailSerializer()

    class Meta(TourFeatureSerializer.Meta):
        pass


class TourSerializer(ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    tour_type = CharField(source="get_tour_type_display")

    class Meta:
        model = Tour
        fields = ("id", "title", "min_price", "images", "tour_type", "days")

    def to_representation(self, instance):
        result = super().to_representation(instance)
        instance.tour_features.prefetch_related("destination")
        result["destinations"] = instance.tour_features.values_list(
            "destination__name", flat=True
        )
        return result

    # def create(self, validated_data):
    #     return super().create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance = super().update(instance, validated_data)
    #     tour_city_list = [
    #         TourCity(tour=instance, city=city, priority=index)
    #         for index, city in enumerate(validated_data["cities"])
    #     ]
    #     MultiCityTour.features.through.objects.bulk_update(tour_city_list)
    #     return instance


class TourDetailSerializer(ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    tour_type = CharField(source="get_tour_type_display")
    features = TourFeatureSerializer(source="tour_features", many=True)
    arrival_dates = ArrivalDatesSerializer(many=True)

    class Meta(TourSerializer.Meta):
        fields = TourSerializer.Meta.fields + (
            "arrival_dates",
            "days",
            "features",
            "description",
        )


class TourDetailRoomsSerializer(TourSerializer):
    features = TourFeatureDetailSerializer(source="tour_features", many=True)

    class Meta(TourSerializer.Meta):
        fields = TourSerializer.Meta.fields + (
            "arrival_dates",
            "days",
            "features",
            "description",
        )

    def to_representation(self, instance):
        result = super().to_representation(instance)
        start = self.context.get("start")
        params = self.context.get("request").query_params
        rooms = get_tour_available_rooms(
            instance.tour_features.all().select_related("hotel"), start, params
        )
        for feature in result.get("features"):
            hotel = feature["hotel"]
            if hotel:
                hotel["room_types"] = rooms.get(hotel["id"])
        return result


class ArrivalDatesDetailSerializer(ArrivalDatesSerializer):
    tour = SerializerMethodField()

    class Meta(ArrivalDatesSerializer.Meta):
        fields = ArrivalDatesSerializer.Meta.fields + ("tour",)

    def get_tour(self, obj):
        return TourDetailRoomsSerializer(
            obj.tour,
            context={"start": obj.date, "request": self.context.get("request")},
        ).data
