from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault, DecimalField, IntegerField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from hotels.serializers import RoomReservationSerializer
from orders.models import Order, OrderRoom
from orders.services import book_rooms, get_order_price
from tours.arrival_dates.models import ArrivalDates
from tours.arrival_dates.serializers import ArrivalDateDetailSerializer
from users.models import User


class OrderRoomsSerializer(ModelSerializer):
    reservation = RoomReservationSerializer()

    class Meta:
        model = OrderRoom
        fields = ("reservation",)

    def to_representation(self, instance):
        return super().to_representation(instance)["reservation"]

    def to_internal_value(self, data):
        data = {"reservation": data}
        return super().to_internal_value(data)


class OrderSerializer(ModelSerializer):
    price = DecimalField(read_only=True, decimal_places=2, max_digits=10)
    count_persons = IntegerField()

    class Meta:
        model = Order
        fields = ("id", "arrival_date", "price", "count_persons")

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result["arrival_date"] = ArrivalDateDetailSerializer(
            ArrivalDates.objects.get(pk=result["arrival_date"])
        ).data
        return result


class OrderDetailSerializer(OrderSerializer):
    ordered_rooms = OrderRoomsSerializer(many=True)
    user = PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=CurrentUserDefault(), write_only=True
    )

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ("user", "ordered_rooms")

    @transaction.atomic
    def create(self, validated_data):
        ordered_rooms = validated_data.pop("ordered_rooms")
        user = self.context["request"].user
        validated_data["price"] = get_order_price(
            validated_data.get("arrival_date"),
            validated_data.get("count_persons"),
            ordered_rooms,
        )
        order = super().create(validated_data)
        book_rooms(order, ordered_rooms, user)
        return order

    def validate(self, data):
        if len(data["ordered_rooms"]) != data["arrival_date"].tour.hotels.count():
            raise ValidationError("Count ordered rooms not equal count hotels")
        return super().validate(data)
