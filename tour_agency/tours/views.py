from rest_framework.viewsets import ModelViewSet

from tours.models import MultiCityTour
from tours.serializers import MultiCityTourSerializer


class MultiCityTourViewSet(ModelViewSet):
    queryset = MultiCityTour.objects.all()
    serializer_class = MultiCityTourSerializer
