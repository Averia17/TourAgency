from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ModelViewSet

from locations.models import Continent, Country, Destination
from locations.serializers import (
    ContinentDetailSerializer,
    CountrySerializer,
    DestinationSerializer,
)


class ContinentViewSet(ReadOnlyModelViewSet):
    queryset = Continent.objects.all()
    serializer_class = ContinentDetailSerializer


class CountryViewSet(ListModelMixin, GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class DestinationViewSet(ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
