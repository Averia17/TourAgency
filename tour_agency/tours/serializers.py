from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from core.constants import MEALS
from core.serializer_fields import ChoiceArrayField
from hotels.serializers import SimpleHotelSerializer
from images.serializers import ImageSerializer
from locations.serializers import DestinationSerializer
from tours.models import (
    MultiCityTour,
    TourFeature,
    OneCityTour,
    MultiCityArrivalDate,
    OneCityArrivalDate,
)


class MultiCityArrivalDatesSerializer(ModelSerializer):
    class Meta:
        model = MultiCityArrivalDate
        fields = ("date",)

    def to_representation(self, instance):
        return super().to_representation(instance)["date"]


class OneCityArrivalDatesSerializer(MultiCityArrivalDatesSerializer):
    class Meta(MultiCityArrivalDatesSerializer.Meta):
        model = OneCityArrivalDate


class TourFeatureSerializer(ModelSerializer):
    hotel = SimpleHotelSerializer()
    destination = DestinationSerializer()
    food = ChoiceArrayField(choices=MEALS)

    class Meta:
        model = TourFeature
        fields = (
            "title",
            "description",
            "day",
            "destination",
            "hotel",
            "food",
        )


class MultiCityTourSerializer(ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    tour_type = CharField(source="get_tour_type_display")

    class Meta:
        model = MultiCityTour
        fields = ("id", "title", "price", "images", "tour_type", "days")

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


class MultiCityTourDetailSerializer(ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    tour_type = CharField(source="get_tour_type_display")
    features = TourFeatureSerializer(source="tour_features", many=True)
    arrival_dates = MultiCityArrivalDatesSerializer(many=True)

    class Meta(MultiCityTourSerializer.Meta):
        fields = (
            "id",
            "title",
            "price",
            "arrival_dates",
            "images",
            "tour_type",
            "days",
            "nights",
            "tour_type",
            "features",
            "description",
        )


class OneCityTourSerializer(ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    arrival_dates = OneCityArrivalDatesSerializer(many=True)

    class Meta:
        model = OneCityTour
        fields = (
            "id",
            "title",
            "description",
            "arrival_dates",
            "destination",
            "hotel",
            "days",
            "nights",
            "images",
        )
