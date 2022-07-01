from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from tours.filters import TourFilter
from tours.models import MultiCityTour, OneCityTour
from tours.serializers import MultiCityTourSerializer, OneCityTourSerializer


class MultiCityTourViewSet(ModelViewSet):
    queryset = MultiCityTour.objects.all()
    serializer_class = MultiCityTourSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TourFilter


class OneCityTourViewSet(ModelViewSet):
    queryset = OneCityTour.objects.all()
    serializer_class = OneCityTourSerializer
