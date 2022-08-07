from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from tours.arrival_dates.models import ArrivalDates
from tours.services import AvailableRoomsService


class ArrivalDatesSerializer(ModelSerializer):
    min_price = SerializerMethodField()

    class Meta:
        model = ArrivalDates
        fields = ("id", "date", "discount", "min_price")

    def get_min_price(self, obj):
        hotel_rooms = AvailableRoomsService(
            self.context.get("request").query_params,
        ).get_available_rooms_data(
            obj.tour.tour_features.all().select_related("hotel"),
            obj.date,
        )
        hotel_price = sum(
            [getattr(rooms.first(), "cost_per_day", 0) for rooms in hotel_rooms]
        )

        return obj.tour.price + hotel_price
