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
        available_rooms_service = AvailableRoomsDataService(self.request.query_params)
        available_rooms_data = available_rooms_service.get_available_rooms_data(
            arrival_date.tour.tour_features.all().select_related("hotel"),
            arrival_date.date,
        )
        available_rooms_data = available_rooms_service.group_rooms(available_rooms_data)
        # if not all(data["rooms"] for data in available_rooms_data.values()):
        #     raise ValidationError("One of hotels has no available rooms")
        return Response(available_rooms_data)
