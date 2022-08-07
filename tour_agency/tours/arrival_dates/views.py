from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from tours.arrival_dates.models import ArrivalDates
from tours.services import AvailableRoomsDataService


class ArrivalDateViewSet(GenericViewSet):
    queryset = ArrivalDates.objects.all().select_related("tour")

    @action(detail=True, methods=["GET"])
    def available_rooms(self, request, pk=None):
        arrival_date = self.get_object()
        available_rooms_data = AvailableRoomsDataService(
            self.request.query_params
        ).get_available_rooms_data(
            arrival_date.tour.tour_features.all().select_related("hotel"),
            arrival_date.date,
        )
        return Response(available_rooms_data)
