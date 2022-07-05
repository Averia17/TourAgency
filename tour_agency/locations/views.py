from rest_framework.viewsets import ReadOnlyModelViewSet

from locations.models import Continent
from locations.serializers import ContinentDetailSerializer


class ContinentViewSet(ReadOnlyModelViewSet):
    queryset = Continent.objects.all()
    serializer_class = ContinentDetailSerializer
