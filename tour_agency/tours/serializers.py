from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from core.constants import MEALS
from core.serializer_fields import ChoiceArrayField
from hotels.serializers import SimpleHotelSerializer
from images.serializers import ImageSerializer
from locations.serializers import DestinationSerializer
from tours.models import TourFeature, ArrivalDates, Tour


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
            "day",
            "destination",
            "hotel",
            "food",
        )


class TourSerializer(ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    tour_type = CharField(source="get_tour_type_display")

    class Meta:
        model = Tour
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


class TourDetailSerializer(ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    tour_type = CharField(source="get_tour_type_display")
    features = TourFeatureSerializer(source="tour_features", many=True)
    arrival_dates = ArrivalDatesSerializer(many=True)

    class Meta(TourSerializer.Meta):
        fields = (
            "id",
            "title",
            "min_price",
            "arrival_dates",
            "images",
            "tour_type",
            "days",
            "features",
            "description",
        )
