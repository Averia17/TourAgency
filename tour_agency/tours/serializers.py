from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from core.constants import MEALS
from core.serializer_fields import ChoiceArrayField
from hotels.serializers import (
    SimpleHotelSerializer,
    HotelDetailSerializer,
)
from images.serializers import ImageSerializer
from locations.serializers import DestinationSerializer
from tours.arrival_dates.serializers import ArrivalDatesSerializer
from tours.models import TourFeature, Tour


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
            "start",
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
        fields = ("id", "title", "images", "tour_type", "days")

    def to_representation(self, instance):
        result = super().to_representation(instance)
        instance.tour_features.prefetch_related("destination")
        result["destinations"] = instance.tour_features.values_list(
            "destination__name", flat=True
        )
        return result


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
