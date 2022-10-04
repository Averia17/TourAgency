from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from core.constants import ORDER_STATUSES
from core.models import BaseModel
from hotels.models import RoomReservation
from users.models import User


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    arrival_date = models.ForeignKey(
        "tours.ArrivalDates",
        related_name="orders",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    status = models.CharField(
        _("Status"), max_length=15, choices=ORDER_STATUSES, default="BOOKED"
    )
    count_tickets = models.PositiveSmallIntegerField(_("Count Tickets"))

    def __str__(self):
        return f"{self.pk} {self.arrival_date}"

    def clean(self):
        if (
            self.arrival_date.count_available is not None
            and self.arrival_date.count_available - self.count_tickets < 0
        ):
            raise ValidationError("Tour with this date has no available places")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

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


@receiver(post_delete, sender=OrderRoom)
def post_delete_reservation(sender, instance, *args, **kwargs):
    if instance.reservation:
        instance.reservation.delete()
