from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault, DecimalField, IntegerField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from hotels.serializers import RoomReservationSerializer
from orders.models import Order, OrderRoom
from orders.services import book_rooms, get_order_price
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
    ordered_rooms = OrderRoomsSerializer(many=True)
    price = DecimalField(read_only=True, decimal_places=2, max_digits=10)
    # price = DecimalField(decimal_places=2, max_digits=10)
    count_persons = IntegerField(write_only=True)
    user = PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=CurrentUserDefault()
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "arrival_date",
            "price",
            "ordered_rooms",
            "count_persons",
        )

    @transaction.atomic
    def create(self, validated_data):
        ordered_rooms = validated_data.pop("ordered_rooms")
        user = self.context["request"].user
        validated_data["price"] = get_order_price(
            validated_data.get("arrival_date"),
            validated_data.pop("count_persons"),
            ordered_rooms,
        )
        order = super().create(validated_data)
        book_rooms(order, ordered_rooms, user)
        return order

    def validate(self, data):
        if len(data["ordered_rooms"]) != data["arrival_date"].tour.hotels.count():
            raise ValidationError("Count ordered rooms not equal count hotels")
        return super().validate(data)
