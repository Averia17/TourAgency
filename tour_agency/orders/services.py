from datetime import timedelta

from rest_framework.exceptions import ValidationError

from hotels.models import RoomType
from orders.models import OrderRoom


def book_rooms(order, rooms_to_order: list, user):
    rooms = []
    start = order.arrival_date.date
    for feature in order.arrival_date.tour.tour_features.all():
        end = start + timedelta(days=feature.days)
        room = [
            room_to_order
            for room_to_order in rooms_to_order
            if room_to_order["feature"] == feature
        ]
        if len(room) != 1:
            raise ValidationError("For each feature must be one room")
        room = room[0]["room"]
        rooms.append(
            OrderRoom(
                start=start, end=end, room=room, user=user, order=order, feature=feature
            )
        )
        start = end
    return OrderRoom.objects.bulk_create(rooms)


def get_order_price(arrival_date, count_tickets, order_rooms):
    price = (arrival_date.tour.price - arrival_date.discount) * count_tickets

    # room prices sum
    for order_room in order_rooms:
        price += order_room.get("room").cost_per_day * order_room.get("feature").days
    return price
