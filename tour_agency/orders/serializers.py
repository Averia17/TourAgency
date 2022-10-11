from django.db import transaction
from rest_framework.fields import CurrentUserDefault, DecimalField, IntegerField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from core.constants import ORDER_SUBJECT, ORDER_MESSAGE
from orders.models import Order, OrderRoom
from orders.services import book_rooms, get_order_price
from tours.arrival_dates.models import ArrivalDates
from tours.arrival_dates.serializers import ArrivalDateDetailSerializer
from users.models import User
from tour_agency.tasks import send_ordered_tour_email


class OrderRoomsSerializer(ModelSerializer):
    class Meta:
        model = OrderRoom
        fields = ("room", "feature", "start", "end")


class OrderSerializer(ModelSerializer):
    price = DecimalField(read_only=True, decimal_places=2, max_digits=10)
    count_tickets = IntegerField()

    class Meta:
        model = Order
        fields = ("id", "arrival_date", "price", "count_tickets")

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
        send_ordered_tour_email.delay(
            user.email,
            ORDER_SUBJECT,
            ORDER_MESSAGE.format(tour=order.arrival_date.tour.title),
            True,
        )
        return order

    # def validate(self, data):
    #     if len(data["ordered_rooms"]) != data["arrival_date"].tour.hotels.count():
    #         raise ValidationError("Count ordered rooms not equal count hotels")
    #     return super().validate(data)
