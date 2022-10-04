from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.filter import CanViewOwnerOrAdminFilterBackend
from core.permissions import IsManagerOrAdmin
from orders.models import Order
from orders.serializers import (
    OrderSerializer,
    OrderDetailSerializer,
)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    serializer_classes = {
        "retrieve": OrderDetailSerializer,
        "create": OrderDetailSerializer,
    }
    permission_to_method = {
        "update": [IsManagerOrAdmin],
        "destroy": [IsManagerOrAdmin],
    }
    filter_backends = (CanViewOwnerOrAdminFilterBackend,)

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
        order.status = kwargs["status"]
        serializer = self.get_serializer(order)
        return Response(serializer.data)
