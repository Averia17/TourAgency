from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from tours.arrival_dates.models import ArrivalDates
from tours.arrival_dates.serializers import ArrivalDateAvailableRoomsSerializer


class ArrivalDateViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = ArrivalDates.objects.all().select_related("tour")
    serializer_class = ArrivalDateAvailableRoomsSerializer
