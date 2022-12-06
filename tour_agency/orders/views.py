from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from core.permissions import IsManagerOrAdmin

from orders.models import Order
from orders.serializers import (
    OrderSerializer,
    OrderDetailSerializer,
)
from orders.services import get_order_price


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    serializer_classes = {
        "retrieve": OrderDetailSerializer,
        "create": OrderDetailSerializer,
    }
    permission_to_method = {
        "list": [IsManagerOrAdmin],
        "update": [IsManagerOrAdmin],
        "partial_update": [IsManagerOrAdmin],
        "destroy": [IsManagerOrAdmin],
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_to_method.get(
                self.action, self.permission_classes
            )
        ]

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = request.data["status"]
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], permission_classes=[IsManagerOrAdmin])
    def booked(self, request):
        booked_orders = self.get_queryset().filter(status="BOOKED")
        serializer = self.get_serializer(booked_orders, many=True)
        return Response(serializer.data)


# TODO: microservice
class OrderPriceView(APIView):
    def post(self, request):
        serializer = OrderDetailSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid()
        data = serializer.validated_data
        price = get_order_price(
            data["arrival_date"], data["count_tickets"], data["ordered_rooms"]
        )
        return Response(price)
