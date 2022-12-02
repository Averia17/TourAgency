from rest_framework.viewsets import ModelViewSet

from core.permissions import IsManagerOrAdmin
from tours.features.serializers import (
    TourFeatureSerializer,
    TourFeatureSimpleSerializer,
    TourFeatureCreateSerializer,
)
from tours.features.models import TourFeature


class TourFeatureViewSet(ModelViewSet):
    queryset = TourFeature.objects.all()
    serializer_class = TourFeatureSimpleSerializer
    permission_classes = [IsManagerOrAdmin]

    serializer_classes = {
        "retrieve": TourFeatureSerializer,
        "create": TourFeatureCreateSerializer,
        "update": TourFeatureCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
