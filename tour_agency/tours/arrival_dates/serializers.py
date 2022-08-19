from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from tours.arrival_dates.models import ArrivalDates


class ArrivalDatesSerializer(ModelSerializer):
    count_available = IntegerField()

    class Meta:
        model = ArrivalDates
        fields = ("id", "date", "discount", "count_available")
