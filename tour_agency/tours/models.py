from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.constants import TOUR_TYPES, MEALS
from core.models import BaseModel, ChoiceArrayField
from core.utils import one_day_hence
from hotels.models import Hotel
from locations.models import City, Destination


class ArrivalDates(models.Model):
    date = models.DateTimeField(_("Arrival date"), default=timezone.now)
    discount = models.PositiveSmallIntegerField(default=0)
    tour = models.ForeignKey(
        "Tour", on_delete=models.CASCADE, related_name="arrival_dates"
    )

    class Meta:
        app_label = "tours"
        verbose_name_plural = "ArrivalDates"

    def clean(self):
        if self.discount > self.tour.min_price:
            raise ValidationError("Discount cannot be bigger than tour minimal price")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)


class Tour(BaseModel):
    title = models.CharField(_("Title"), unique=True, max_length=256)
    description = models.CharField(
        _("Description"), max_length=512, null=True, blank=True
    )
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    tour_type = models.CharField(max_length=16, choices=TOUR_TYPES, default="LAND")

    @property
    def days(self):
        return self.tour_features.latest().day

    @property
    def min_price(self):
        hotel_price = 0
        for feature in self.tour_features.filter(hotel__isnull=False).select_related(
            "hotel"
        ):
            room = feature.hotel.room_types.order_by("cost_per_day").first()
            if room:
                hotel_price += room.cost_per_day

        return self.price + hotel_price

    class Meta:
        app_label = "tours"

    def __str__(self):
        return f"{self.title}"


class TourFeature(BaseModel):
    title = models.CharField(_("Title"), max_length=256)
    description = models.CharField(
        _("Description"), max_length=512, null=True, blank=True
    )
    order = models.PositiveSmallIntegerField(default=1)
    days = models.PositiveSmallIntegerField(default=1)
    food = ChoiceArrayField(
        base_field=models.CharField(max_length=10, choices=MEALS, default="BREAKFAST")
    )
    hotel = models.ForeignKey(
        Hotel,
        related_name="tour_features",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    destination = models.ForeignKey(
        Destination, related_name="tour_features", on_delete=models.CASCADE
    )
    tour = models.ForeignKey(
        Tour, related_name="tour_features", on_delete=models.CASCADE
    )

    class Meta(Tour.Meta):
        app_label = "tours"
        verbose_name_plural = "TourFeature"
        get_latest_by = ["order"]
        ordering = ["tour", "order"]
        constraints = [
            models.UniqueConstraint(fields=["tour", "order"], name="uq_tour_order")
        ]

    def __str__(self):
        return f"{self.days}: {self.title}"
