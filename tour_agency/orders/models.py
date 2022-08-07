from django.db import models
from django.utils.translation import gettext_lazy as _

from core.constants import ORDER_STATUSES
from core.models import BaseModel
from hotels.models import RoomReservation
from tours.arrival_dates.models import ArrivalDates
from users.models import User


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    arrival_date = models.ForeignKey(
        ArrivalDates, related_name="orders", on_delete=models.CASCADE
    )
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    status = models.CharField(
        _("Status"), max_length=15, choices=ORDER_STATUSES, default="BOOKED"
    )

    def __str__(self):
        return f"{self.pk} {self.arrival_date}"

    class Meta:
        app_label = "orders"


class OrderRoom(BaseModel):
    reservation = models.OneToOneField(
        RoomReservation, primary_key=True, on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order, related_name="ordered_rooms", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.order} {self.reservation}"

    class Meta:
        app_label = "orders"
        verbose_name_plural = "OrderRooms"
