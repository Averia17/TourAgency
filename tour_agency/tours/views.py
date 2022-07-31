from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from tours.filters import TourFilter
from tours.models import Tour, ArrivalDates
from tours.serializers import (
    TourSerializer,
    TourDetailSerializer,
    ArrivalDatesDetailSerializer,
)


class TourViewSet(ModelViewSet):
    queryset = Tour.objects.all().prefetch_related(
        "tour_features", "arrival_dates", "images"
    )
    serializer_class = TourSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TourFilter

    serializer_classes = {
        "retrieve": TourDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)


class ArrivalDateViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = ArrivalDates.objects.all().select_related("tour")
    serializer_class = ArrivalDatesDetailSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     arrival_date = self.get_object()
    #     params = self.request.query_params
    #     # hotels = arrival_date.tour.hotels
    #     # rooms_prefetch = []
    #     # start = arrival_date.date
    #     # for feature in arrival_date.tour.tour_features.all():
    #     #     end = start + datetime.timedelta(days=feature.days)
    #     #     hotel = feature.hotel
    #     #     if hotel:
    #     #         hotel.available_rooms(start, end, params)
    #     #     start = end
    #     # arrival_date = arrival_date.tour.tour_features.prefetch_related(
    #     #     Prefetch(
    #     #         "hotel__room_types",
    #     #         queryset=RoomType.objects.filter(pk__in=rooms_prefetch),
    #     #     )
    #     # )
    #     print(arrival_date)
    #     serializer = self.get_serializer(arrival_date)
    #     return Response(serializer.data)
