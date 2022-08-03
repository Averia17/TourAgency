from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count, F, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.constants import CONVENIENCES_TYPES
from core.models import BaseModel
from core.utils import one_day_hence
from locations.models import StreetMixin
from users.models import User


class Convenience(BaseModel):
    icon = models.OneToOneField(
        "images.Image", on_delete=models.SET_NULL, blank=True, null=True
    )
    name = models.CharField(_("Name"), unique=True, max_length=256)
    type = models.CharField(
        _("Type"), max_length=16, choices=CONVENIENCES_TYPES, default="HOTEL"
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = "hotels"
        verbose_name_plural = "Conveniences"


class Hotel(BaseModel, StreetMixin):
    name = models.CharField(_("Name"), unique=True, max_length=256)
    stars_number = models.PositiveSmallIntegerField(
        _("Number of stars"), validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    description = models.CharField(
        _("Description"), max_length=1024, null=True, blank=True
    )
    conveniences = models.ManyToManyField(
        Convenience, related_name="hotels", blank=True
    )

    def available_rooms(self, start, end):
        rooms = (
            self.room_types.annotate(
                reserved_dates=Count(
                    "rented_dates",
                    filter=Q(
                        rented_dates__end__gte=start, rented_dates__start__lte=end
                    ),
                )
            )
            .filter(count_rooms__gt=F("reserved_dates"))
            .order_by("cost_per_day")
        )
        return rooms

    def __str__(self):
        return f"{self.name}"

    class Meta(StreetMixin.Meta):
        app_label = "hotels"
        verbose_name_plural = "Hotels"


class RoomType(BaseModel):
    name = models.CharField(_("Name"), max_length=32)
    hotel = models.ForeignKey(
        Hotel, related_name="room_types", on_delete=models.CASCADE
    )
    count_places = models.PositiveSmallIntegerField(_("Count places"), default=2)
    count_rooms = models.PositiveSmallIntegerField(_("Count rooms"), default=10)
    is_family = models.BooleanField(_("Is family"), default=False)
    cost_per_day = models.DecimalField(
        _("Cost per day"), max_digits=10, decimal_places=2
    )
    description = models.CharField(
        _("Description"), max_length=512, null=True, blank=True
    )
    square = models.FloatField(_("Square"))
    conveniences = models.ManyToManyField(Convenience, related_name="rooms", blank=True)

    def __str__(self):
        return f"{self.pk} {self.name}: {self.hotel}"

    def is_available(self, start, end):
        reserved_dates = self.rented_dates.filter(end__gte=start, start__lte=end)
        return self.count_rooms > reserved_dates.count()

    class Meta:
        app_label = "hotels"
        verbose_name_plural = "Rooms"
        ordering = ["cost_per_day"]
        constraints = [
            models.UniqueConstraint(fields=["name", "hotel"], name="uq_name_hotel")
        ]


# TODO: add related_name
class Rent(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class RoomReservation(Rent):
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=one_day_hence)
    room = models.ForeignKey(
        RoomType, related_name="rented_dates", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room}: {self.start.date()} - {self.end.date()}"

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

    class Meta:
        app_label = "hotels"
        verbose_name_plural = "RoomReservations"


# will be rent a plane
