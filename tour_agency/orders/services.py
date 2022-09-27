from hotels.models import RoomReservation
from orders.models import OrderRoom


def book_rooms(order, rooms_to_order: list, user):
    # create rooms reservations
    reservations = [
        RoomReservation.objects.create(
            start=reservation["reservation"]["start"],
            end=reservation["reservation"]["end"],
            room=reservation["reservation"]["room"],
            user=user,
        )
        for reservation in rooms_to_order
    ]
    # order rooms
    ordered_rooms = [
        OrderRoom(order=order, reservation=reservation) for reservation in reservations
    ]
    return OrderRoom.objects.bulk_create(ordered_rooms)


def get_order_price(arrival_date, count_persons, order_rooms):
    price = (arrival_date.tour.price - arrival_date.discount) * count_persons

    price += sum(
        [
            order_room.get("reservation").get("room").cost_per_day
            for order_room in order_rooms
        ]
    )
    return price
