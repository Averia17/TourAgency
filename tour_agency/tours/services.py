import datetime
from hotels.services import filter_rooms


class AvailableRoomsService:
    def __init__(self, params):
        self.filter_params = params

    def get_available_rooms_data(self, features, start):
        hotel_data = []
        for feature in features:
            end = start + datetime.timedelta(days=feature.days)
            hotel = feature.hotel
            if hotel:
                hotel_data.append(self.get_rooms(hotel, start, end))
            start = end
        return hotel_data

    def get_rooms(self, hotel, start, end):
        rooms = hotel.room_types.all()
        if start and end:
            rooms = hotel.available_rooms(start, end)
        if self.filter_params:
            rooms = filter_rooms(self.filter_params, rooms)
        return rooms


class AvailableRoomsDataService(AvailableRoomsService):
    def get_rooms(self, hotel, start, end):
        from hotels.serializers import HotelDetailSerializer

        return {
            "start": start,
            "end": end,
            **HotelDetailSerializer(
                hotel,
                context={
                    "start": start,
                    "end": end,
                    "filter_params": self.filter_params,
                },
            ).data,
        }
