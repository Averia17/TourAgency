from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from tours.arrival_dates.models import ArrivalDates


class ArrivalDatesSerializer(ModelSerializer):
    count_available = IntegerField()

    class Meta:
        model = ArrivalDates
        fields = ("id", "date", "discount", "count_available")


class ArrivalDatesCreateSerializer(ModelSerializer):
    class Meta:
        model = ArrivalDates
        fields = "__all__"

class ArrivalDateDetailSerializer(ModelSerializer):
    from tours.serializers import TourSerializer

    tour = TourSerializer()

    class Meta:
        model = ArrivalDates
        fields = ("id", "date", "tour")


class ArrivalDateAvailableRoomsSerializer(ArrivalDateDetailSerializer):
    tour = SerializerMethodField()

    class Meta(ArrivalDateDetailSerializer.Meta):
        pass

    def get_tour(self, obj):
        from tours.serializers import TourDetailFeaturesSerializer

        return TourDetailFeaturesSerializer(obj.tour, context={"start": obj.date}).data
