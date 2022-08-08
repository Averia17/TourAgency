from rest_framework.serializers import ModelSerializer

from tours.arrival_dates.models import ArrivalDates


class ArrivalDatesSerializer(ModelSerializer):
    class Meta:
        model = ArrivalDates
        fields = ("id", "date", "discount")
