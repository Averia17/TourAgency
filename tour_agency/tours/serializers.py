from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from core.constants import MEALS
from core.serializer_fields import ChoiceArrayField
from hotels.serializers import SimpleHotelSerializer
from locations.serializers import CitySerializer, DestinationSerializer
from tours.models import MultiCityTour, TourFeature, OneCityTour


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
    features = TourFeatureSerializer(source="tour_features", many=True)
    # tour_type = ChoiceField(choices=TOUR_TYPES)
    tour_type = CharField(source="get_tour_type_display")

    class Meta:
        model = MultiCityTour
        fields = (
            "id",
            "title",
            "description",
            "tour_type",
            "start",
            "end",
            "price",
            "features",
        )

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


class OneCityTourSerializer(ModelSerializer):
    class Meta:
        model = OneCityTour
        fields = ("id", "title", "description", "start", "end", "destination", "hotel")
