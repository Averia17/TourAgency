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
            rooms = hotel.available_rooms(start, end).prefetch_related(
                "images", "conveniences"
            )
        if self.filter_params:
            rooms = filter_rooms(self.filter_params, rooms)
        return rooms


class AvailableRoomsDataService(AvailableRoomsService):
    def get_rooms(self, hotel, start, end):
        from hotels.serializers import RoomTypeSerializer

        return {
            "hotel": hotel.pk,
            "dates": [{"start": start, "end": end}],
            "rooms": RoomTypeSerializer(
                super().get_rooms(hotel, start, end), many=True
            ).data,
        }

    def group_rooms(self, rooms_data):
        grouped_hotels = {}
        for data in rooms_data:
            hotel_id = data.pop("hotel")
            if hotel_id in grouped_hotels:
                grouped_hotels[hotel_id]["rooms"] = [
                    room
                    for room in grouped_hotels[hotel_id]["rooms"]
                    if room in data["rooms"]
                ]
                grouped_hotels[hotel_id]["dates"].append(data["dates"])
            else:
                grouped_hotels[hotel_id] = data
        return grouped_hotels
