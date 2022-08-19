from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from images.models import HotelImage
from tours.arrival_dates.models import ArrivalDates
from tours.filters import TourFilter
from tours.models import Tour, TourFeature
from tours.serializers import (
    TourSerializer,
    TourDetailSerializer,
)


class TourViewSet(ModelViewSet):
    queryset = Tour.objects.all().prefetch_related(
        "images",
        Prefetch(
            "tour_features",
            queryset=TourFeature.objects.select_related(
                "destination",
                "hotel",
                "destination__image",
            ).prefetch_related("hotel__images"),
        ),
        Prefetch(
            "arrival_dates",
            queryset=ArrivalDates.objects.prefetch_related("orders"),
        ),
    )

    serializer_class = TourSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TourFilter

    serializer_classes = {
        "retrieve": TourDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
