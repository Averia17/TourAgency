from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from hotels.models import Hotel, RoomType
from hotels.serializers import (
    HotelSerializer,
    HotelDetailSerializer,
    RoomTypeDetailSerializer,
)


class HotelsViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    serializer_classes = {
        "retrieve": HotelDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.save(images=self.request.FILES.getlist("images"))

    def perform_update(self, serializer):
        serializer.save(images=self.request.FILES.getlist("images"))


class RoomViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeDetailSerializer
