from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsManagerOrAdmin
from tours.filters import TourFilter
from tours.models import Tour
from tours.features.models import TourFeature
from tours.serializers import TourSerializer, TourDetailSerializer


class TourViewSet(ModelViewSet):
    queryset = Tour.objects.all().prefetch_related(
        "images",
        "arrival_dates",
        Prefetch(
            "tour_features",
            queryset=TourFeature.objects.select_related(
                "destination",
                "hotel",
                "destination__image",
            ).prefetch_related("hotel__images"),
        ),
    )

    serializer_class = TourSerializer
    search_fields = [
        "title",
        "tour_features__destination__name",
        "tour_features__destination__country__name",
    ]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TourFilter

    serializer_classes = {
        "retrieve": TourDetailSerializer,
    }
    permission_to_method = {
        "create": [IsManagerOrAdmin],
        "update": [IsManagerOrAdmin],
        "destroy": [IsManagerOrAdmin],
    }

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_to_method.get(
                self.action, self.permission_classes
            )
        ]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
