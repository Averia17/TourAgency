from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from hotels.serializers import RoomReservationSerializer
from orders.models import Order, OrderRoom
from orders.services import order_rooms
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
    user = PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=CurrentUserDefault()
    )

    class Meta:
        model = Order
        fields = ("id", "user", "arrival_date", "price", "ordered_rooms")

    @transaction.atomic
    def create(self, validated_data):
        ordered_rooms = validated_data.pop("ordered_rooms")
        user = self.context["request"].user
        instance = super().create(validated_data)
        order_rooms(instance, ordered_rooms, user)
        return instance

    def validate(self, data):
        if len(data["ordered_rooms"]) != data["arrival_date"].tour.hotels.count():
            raise ValidationError("Count ordered rooms not equal count hotels")
        return super().validate(data)
