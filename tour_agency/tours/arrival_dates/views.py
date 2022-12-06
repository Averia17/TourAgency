from rest_framework.viewsets import ModelViewSet

from core.permissions import IsManagerOrAdmin
from tours.arrival_dates.models import ArrivalDates
from tours.arrival_dates.serializers import (
    ArrivalDateAvailableRoomsSerializer,
    ArrivalDatesCreateSerializer,
)


class ArrivalDateViewSet(ModelViewSet):
    queryset = ArrivalDates.objects.all().select_related("tour")
    serializer_class = ArrivalDateAvailableRoomsSerializer

    serializer_classes = {
        "list": ArrivalDatesCreateSerializer,
        "retrieve": ArrivalDatesCreateSerializer,
        "create": ArrivalDatesCreateSerializer,
    }
    permission_to_method = {
        "list": [IsManagerOrAdmin],
        "create": [IsManagerOrAdmin],
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
