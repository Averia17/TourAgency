from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from tours.filters import TourFilter
from tours.models import MultiCityTour, OneCityTour
from tours.serializers import (
    MultiCityTourSerializer,
    OneCityTourSerializer,
    MultiCityTourDetailSerializer,
)


class MultiCityTourViewSet(ModelViewSet):
    queryset = MultiCityTour.objects.all()
    serializer_class = MultiCityTourSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TourFilter

    serializer_classes = {
        "retrieve": MultiCityTourDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)


class OneCityTourViewSet(ModelViewSet):
    queryset = OneCityTour.objects.all()
    serializer_class = OneCityTourSerializer
