from django.db.models import Prefetch
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.permissions import IsManagerOrAdmin
from core.utils import string_to_list, true
from hotels.models import Hotel, RoomType
from hotels.serializers import (
    HotelSerializer,
    HotelDetailSerializer,
    RoomDetailSerializer,
    RoomTypeSerializer,
)
from hotels.services import filter_rooms


class HotelsViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    serializer_classes = {
        "retrieve": HotelDetailSerializer,
    }
    permission_to_method = {
        "create": [IsManagerOrAdmin],
        "update": [IsManagerOrAdmin],
        "destroy": [IsManagerOrAdmin],
    }

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_to_method.get(
                self.action, self.permission_classes
            )
        ]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    def filter_queryset(self, queryset):
        params = self.request.query_params
        queryset = queryset.prefetch_related(
            Prefetch(
                "room_types",
                queryset=filter_rooms(params),
            )
        )

        return queryset

    def perform_create(self, serializer):
        serializer.save(images=self.request.FILES.getlist("images"))

    def perform_update(self, serializer):
        serializer.save(images=self.request.FILES.getlist("images"))


class RoomViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    serializer_classes = {
        "retrieve": RoomDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
