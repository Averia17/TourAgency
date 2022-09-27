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


def get_order_price(arrival_date, count_tickets, order_rooms):
    price = (arrival_date.tour.price - arrival_date.discount) * count_tickets

    for order_room in order_rooms:
        reservation = order_room.get("reservation")
        room_cost = reservation.get("room").cost_per_day
        ordered_days = (reservation.get("end") - reservation.get("start")).days
        price += room_cost * ordered_days
    return price
