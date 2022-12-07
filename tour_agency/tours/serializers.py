import datetime

from rest_framework.fields import (
    CharField,
    SerializerMethodField,
    IntegerField,
    DecimalField,
)
from rest_framework.serializers import ModelSerializer

from hotels.serializers import HotelDetailSerializer
from images.models import TourImage
from images.serializers import ImageSerializer, ImageUploadSerializer
from tours.arrival_dates.serializers import ArrivalDatesSerializer
from tours.features.serializers import TourFeatureSerializer
from tours.models import Tour


class TourFeatureDetailSerializer(TourFeatureSerializer):
    hotel = SerializerMethodField()

    class Meta(TourFeatureSerializer.Meta):
        pass

    def get_hotel(self, obj):
        return HotelDetailSerializer(
            obj.hotel,
            context={
                "start": self.context.get("start"),
                "end": self.context.get("end"),
                "filter_params": self.context.get("filter_params"),
            },
        ).data


class TourSerializer(ImageUploadSerializer):
    images = ImageSerializer(many=True, read_only=True)
    max_passengers = IntegerField(write_only=True)
    price = DecimalField(write_only=True, decimal_places=2, max_digits=10)
    min_price = DecimalField(read_only=True, decimal_places=2, max_digits=10)

    image_model = TourImage
    additional_field = "tour"

    class Meta:
        model = Tour
        fields = (
            "id",
            "title",
            "images",
            "tour_type",
            "days",
            "description",
            "max_passengers",
            "price",
            "min_price",
        )

    def to_representation(self, instance):
        self.fields["tour_type"] = CharField(source="get_tour_type_display")
        result = super().to_representation(instance)
        instance.tour_features.prefetch_related("destination")
        result["destinations"] = instance.tour_features.values_list(
            "destination__name", flat=True
        )
        return result


class TourDetailSerializer(ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    tour_type = CharField(source="get_tour_type_display")
    features = TourFeatureSerializer(source="tour_features", many=True)
    arrival_dates = ArrivalDatesSerializer(many=True)

    class Meta(TourSerializer.Meta):
        fields = TourSerializer.Meta.fields + (
            "price",
            "arrival_dates",
            "days",
            "features",
            "description",
        )


class TourDetailFeaturesSerializer(TourSerializer):
    features = SerializerMethodField()

    class Meta(TourSerializer.Meta):
        fields = TourSerializer.Meta.fields + ("features",)

    def get_features(self, obj):
        start = self.context.get("start")
        data = []
        for feature in obj.tour_features.all():
            end = start + datetime.timedelta(days=feature.days)
            data.append(
                TourFeatureDetailSerializer(
                    feature, context={"start": start, "end": end}
                ).data
            )
            start = end
        return data
