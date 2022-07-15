from django.db.models import Prefetch
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.utils import string_to_datetime
from hotels.models import Hotel, RoomType
from hotels.serializers import (
    HotelSerializer,
    HotelDetailSerializer,
    RoomDetailSerializer,
    RoomTypeSerializer,
)


class HotelsViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    serializer_classes = {
        "retrieve": HotelDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    #
    # def retrieve(self, request, *args, **kwargs):
    #     start_date = self.request.query_params.get("start", None)
    #     end_date = self.request.query_params.get("end", None)
    #     hotel = super().get_object()
    #     hotel.prefetch_related(
    #         Prefetch("room_types", queryset=RoomType.objects.filter(is_available=True))
    #     )
    #     super(HotelsViewSet, self).retrieve(request, *args, **kwargs)

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

    #
    # def filter_queryset(self, queryset):
    #     queryset = super().filter_queryset(queryset)
    #     start_date = self.request.query_params.get("start", None)
    #     end_date = self.request.query_params.get("end", None)
    #     if start_date and end_date:
    #         result["is_available"] = instance.is_available(
    #             string_to_datetime(start_date), string_to_datetime(end_date)
    #         )
