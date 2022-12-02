from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from core.constants import ORDER_STATUSES
from core.models import BaseModel
from core.utils import one_day_hence
from hotels.models import RoomType
from tours.features.models import TourFeature
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
    user = models.ForeignKey(
        User, related_name="ordered_rooms", on_delete=models.CASCADE
    )
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=one_day_hence)
    room = models.ForeignKey(
        RoomType, related_name="ordered_rooms", on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order, related_name="ordered_rooms", on_delete=models.CASCADE
    )
    feature = models.ForeignKey(
        TourFeature, related_name="ordered_rooms", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.order} {self.room}"

    class Meta:
        app_label = "orders"
        verbose_name_plural = "OrderRooms"

    def clean(self):
        if self.start > self.end:
            raise ValidationError("Start date cannot be bigger than end date")
        if not self.room.is_available(self.start, self.end):
            raise ValidationError("Room is not available for these dates")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)
