from rest_framework.viewsets import ReadOnlyModelViewSet

from locations.models import Continent
from locations.serializers import ContinentSerializer, ContinentDetailSerializer


class ContinentViewSet(ReadOnlyModelViewSet):
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

    serializer_classes = {
        "retrieve": ContinentDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
