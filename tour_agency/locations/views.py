from rest_framework.viewsets import ReadOnlyModelViewSet

from locations.models import Continent, Country, Destination
from locations.serializers import ContinentDetailSerializer, CountrySerializer, DestinationSerializer


class ContinentViewSet(ReadOnlyModelViewSet):
    queryset = Continent.objects.all()
    serializer_class = ContinentDetailSerializer


class CountryViewSet(ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class DestinationViewSet(ReadOnlyModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
