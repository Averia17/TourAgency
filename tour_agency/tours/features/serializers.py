from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from core.constants import MEALS
from core.serializer_fields import ChoiceArrayField
from hotels.serializers import SimpleHotelSerializer
from locations.serializers import DestinationSerializer
from tours.features.models import TourFeature


class TourFeatureSimpleSerializer(ModelSerializer):
    class Meta:
        model = TourFeature
        fields = ("id", "title", "days", "tour")


class TourFeatureCreateSerializer(ModelSerializer):
    class Meta:
        model = TourFeature
        fields = "__all__"


class TourFeatureSerializer(ModelSerializer):
    hotel = SimpleHotelSerializer()
    destination = DestinationSerializer()
    food = ChoiceArrayField(choices=MEALS)

    class Meta(TourFeatureSimpleSerializer.Meta):
        fields = TourFeatureSimpleSerializer.Meta.fields + (
            "description",
            "destination",
            "hotel",
            "food",
        )
