from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from hotels.models import Hotel, RoomType
from hotels.serializers import (
    HotelSerializer,
    HotelDetailSerializer,
    RoomTypeDetailSerializer,
)


class HotelsViewSet(ReadOnlyModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    serializer_classes = {
        "retrieve": HotelDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)


class RoomViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeDetailSerializer
