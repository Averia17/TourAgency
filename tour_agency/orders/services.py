from hotels.models import RoomReservation
from orders.models import OrderRoom


def order_rooms(order, room_to_order: list, user):
    # create rooms reservations
    reservations = [
        RoomReservation.objects.create(
            start=reservation["reservation"]["start"],
            end=reservation["reservation"]["end"],
            room=reservation["reservation"]["room"],
            user=user,
        )
        for reservation in room_to_order
    ]
    # order rooms
    ordered_rooms = [
        OrderRoom(order=order, reservation=reservation) for reservation in reservations
    ]
    return OrderRoom.objects.bulk_create(ordered_rooms)
