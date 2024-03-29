import logging

from django.db import transaction
from rest_framework.fields import (
    CurrentUserDefault,
    DecimalField,
    IntegerField,
    CharField,
)
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField
from rest_framework.serializers import ModelSerializer

from core.constants import ORDER_SUBJECT, ORDER_MESSAGE, ORDER_FILE_PATH
from orders.models import Order, OrderRoom
from orders.services import book_rooms, get_order_price
from tours.arrival_dates.models import ArrivalDates
from tours.arrival_dates.serializers import ArrivalDateDetailSerializer
from users.models import User
from tour_agency.tasks import send_user_email


logger = logging.getLogger(__name__)


class OrderRoomsSerializer(ModelSerializer):
    class Meta:
        model = OrderRoom
        fields = ("room", "feature")


class OrderSerializer(ModelSerializer):
    price = DecimalField(read_only=True, decimal_places=2, max_digits=10)
    count_tickets = IntegerField()
    status = CharField(source="get_status_display", read_only=True)
    user = SlugRelatedField(read_only=True, slug_field="email")

    class Meta:
        model = Order
        fields = (
            "id",
            "arrival_date",
            "price",
            "count_tickets",
            "status",
            "created",
            "user",
        )

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
            validated_data.get("count_tickets"),
            ordered_rooms,
        )
        order = super().create(validated_data)
        book_rooms(order, ordered_rooms, user)
        logger.info("order %s created", order.id)
        send_user_email.delay(
            user.email,
            ORDER_SUBJECT,
            ORDER_MESSAGE.format(tour=order.arrival_date.tour.title),
            ORDER_FILE_PATH,
        )
        return order
