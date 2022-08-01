from core.utils import true
from hotels.models import RoomType


def filter_rooms(params: dict, queryset=RoomType.objects.all()):
    filter_keys = {"count_places": "count_places__gte"}
    filter_type = {"count_places": int, "is_family": true}
    filter_args = {}
    for param in params:
        if param in filter_type:
            filter_args[filter_keys.get(param, param)] = filter_type[param](
                params.get(param)
            )
    rooms = queryset.filter(**filter_args)
    return rooms
