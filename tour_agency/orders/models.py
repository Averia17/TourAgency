from django.db import models
from core.models import BaseModel
from hotels.models import RoomReservation
from tours.models import ArrivalDates
from users.models import User


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    arrival_date = models.ForeignKey(
        ArrivalDates, related_name="orders", on_delete=models.CASCADE
    )

    class Meta:
        app_label = "orders"


class OrderRooms(BaseModel):
    order = models.ForeignKey(
        Order, related_name="ordered_items", on_delete=models.CASCADE
    )
    reservation = models.OneToOneField(RoomReservation, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.order} {self.reservation}"
