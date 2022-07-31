import datetime

from hotels.serializers import RoomTypeSerializer


def get_tour_available_rooms(features, start, params):
    rooms = {}
    for feature in features:
        end = start + datetime.timedelta(days=feature.days)
        hotel = feature.hotel
        if hotel:
            rooms[hotel.pk] = RoomTypeSerializer(
                hotel.available_rooms(start, end, params), many=True
            ).data
        start = end
    return rooms
