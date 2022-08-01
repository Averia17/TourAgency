from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from tours.filters import TourFilter
from tours.models import Tour
from tours.serializers import (
    TourSerializer,
    TourDetailSerializer,
)


class TourViewSet(ModelViewSet):
    queryset = Tour.objects.all().prefetch_related(
        "tour_features", "arrival_dates", "images"
    )
    serializer_class = TourSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TourFilter

    serializer_classes = {
        "retrieve": TourDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
