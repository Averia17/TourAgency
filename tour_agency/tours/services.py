import datetime
from hotels.serializers import HotelDetailSerializer


def get_available_rooms_data(features, start, filter_params):
    hotel_data = []
    for feature in features:
        end = start + datetime.timedelta(days=feature.days)
        hotel = feature.hotel
        if hotel:
            hotel_data.append(
                {
                    "start": start,
                    "end": end,
                    **HotelDetailSerializer(
                        hotel,
                        context={
                            "start": start,
                            "end": end,
                            "filter_params": filter_params,
                        },
                    ).data,
                }
            )
        start = end
    return hotel_data
