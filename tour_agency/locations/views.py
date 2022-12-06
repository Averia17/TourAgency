from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ModelViewSet

from core.permissions import IsManagerOrAdmin
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
    queryset = Destination.objects.all().select_related("image")
    serializer_class = DestinationSerializer

    permission_to_method = {
        "create": [IsManagerOrAdmin],
        "update": [IsManagerOrAdmin],
        "partial_update": [IsManagerOrAdmin],
        "destroy": [IsManagerOrAdmin],
    }

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_to_method.get(
                self.action, self.permission_classes
            )
        ]
