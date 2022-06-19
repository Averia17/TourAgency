from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Func
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import (
    RangeOperators,
    DateTimeRangeField,
    RangeBoundary,
)

from core.models import BaseModel
from core.utils import one_day_hence
from locations.models import StreetMixin
from psycopg2.extras import DateTimeRange

from users.models import User


class Hotel(BaseModel, StreetMixin):
    name = models.CharField(_("Name"), unique=True, max_length=256)
    stars_number = models.PositiveSmallIntegerField(
        _("Number of stars"), validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    description = models.CharField(
        _("Description"), max_length=512, null=True, blank=True
    )
    image_url = models.URLField(
        _("Image url"),
        help_text="Absolute URL to public image file",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}: {self.get_full_name()}"

    class Meta(StreetMixin.Meta):
        app_label = "hotels"
        verbose_name_plural = "Hotels"


class RoomType(BaseModel):
    name = models.CharField(_("Name"), unique=True, max_length=32)
    hotel = models.ForeignKey(
        Hotel, related_name="room_types", on_delete=models.CASCADE
    )
    count_places = models.PositiveSmallIntegerField(_("Count places"))
    is_family = models.BooleanField(_("Is family"), default=False)
    has_balcony = models.BooleanField(_("Has balcony"), default=False)
    has_own_bathroom = models.BooleanField(_("Has own bathroom"), default=False)
    cost_per_day = models.DecimalField(
        _("Cost per day"), max_digits=10, decimal_places=2
    )
    description = models.CharField(
        _("Description"), max_length=512, null=True, blank=True
    )
    square = models.FloatField(_("Square"))

    # image_url = models.URLField(
    #     _("Image url"), help_text="Absolute URL to public image file"
    # )
    def __str__(self):
        return f"{self.name}: {self.hotel}"

    class Meta:
        app_label = "hotels"
        verbose_name_plural = "RoomsTypes"
        constraints = [
            models.UniqueConstraint(fields=["name", "hotel"], name="uq_name_hotel")
        ]


class Room(BaseModel):
    number = models.CharField(_("Number"), max_length=10)

    room_type = models.ForeignKey(
        RoomType,
        related_name="rooms",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.number}: {self.room_type.name}"

    class Meta:
        app_label = "hotels"
        verbose_name_plural = "Rooms"


class Rent(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TsTzRange(Func):
    function = "TSTZRANGE"
    output_field = DateTimeRangeField()


class RoomReservation(Rent):
    # date_range = DateTimeRangeField()
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=one_day_hence)
    room = models.ForeignKey(
        Room, related_name="rented_dates", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room}: {self.start.date()} - {self.end.date()}"

    def clean(self):
        if self.start > self.end:
            raise ValidationError("Start date cannot be bigger than end date")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(self, *args, **kwargs)

    def is_range_already_reserved(self, start, end):
        #  date_range = TsTzRange(start, end, RangeBoundary(True, True))
        # date_range = DateTimeRange(start, end, bounds="[]")
        # return self.objects.filter(date_range__contained_by=date_range).exists()
        # self.objects.annotate(
        #     period=Func(
        #         F('start'),
        #         F('end'),
        #         function='DATERANGE',
        #         output_field=DateRangeField())
        # ).filter(period__overlap=date_range)
        return self.objects.filter(end__gte=start, start__lte=end).exists()

    class Meta:
        app_label = "hotels"
        verbose_name_plural = "RoomReservations"
        constraints = [
            ExclusionConstraint(
                name="exclude_overlapping_reservations",
                expressions=(
                    (
                        TsTzRange("start", "end", RangeBoundary()),
                        RangeOperators.OVERLAPS,
                    ),
                    ("room", RangeOperators.EQUAL),
                ),
            ),
        ]


# will be rent a plane
