from django.contrib.postgres.fields import ArrayField
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

    class Meta:
        app_label = "tours"
        abstract = True


class MultiCityArrivalDate(ArrivalDates):
    tour = models.ForeignKey(
        "MultiCityTour", on_delete=models.CASCADE, related_name="arrival_dates"
    )

    class Meta(ArrivalDates.Meta):
        verbose_name_plural = "MultiCityArrivalDates"


class OneCityArrivalDate(ArrivalDates):
    tour = models.ForeignKey(
        "OneCityTour", on_delete=models.CASCADE, related_name="arrival_dates"
    )

    class Meta(ArrivalDates.Meta):
        verbose_name_plural = "OneCityTourArrivalDates"


class Tour(models.Model):
    title = models.CharField(_("Title"), unique=True, max_length=256)
    description = models.CharField(
        _("Description"), max_length=512, null=True, blank=True
    )

    class Meta:
        app_label = "tours"
        abstract = True

    def __str__(self):
        return f"{self.title}"


class OneCityTour(BaseModel, Tour):
    destination = models.ForeignKey(
        Destination, related_name="one_city_tours", on_delete=models.CASCADE
    )
    hotel = models.ForeignKey(
        Hotel, related_name="one_city_tours", on_delete=models.PROTECT
    )
    days = models.PositiveSmallIntegerField(default=1)

    @property
    def nights(self):
        return self.days - 1 if self.days else 0

    class Meta(Tour.Meta):
        verbose_name_plural = "OneCityTours"


class MultiCityTour(BaseModel, Tour):
    tour_type = models.CharField(max_length=10, choices=TOUR_TYPES, default="LAND")
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)

    @property
    def last_day(self):
        return self.tour_features.order_by("-day").first()

    @property
    def days(self):
        return self.last_day.day if self.last_day else 0

    @property
    def nights(self):
        nights = 0
        if self.last_day:
            nights = self.days - 1
            if self.last_day.hotel:
                nights = self.days
        return nights

    class Meta(Tour.Meta):
        verbose_name_plural = "MultiCityTours"


class TourFeature(BaseModel):
    title = models.CharField(_("Title"), max_length=256)
    description = models.CharField(
        _("Description"), max_length=512, null=True, blank=True
    )
    day = models.PositiveSmallIntegerField()
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
        MultiCityTour, related_name="tour_features", on_delete=models.CASCADE
    )

    class Meta(Tour.Meta):
        app_label = "tours"
        verbose_name_plural = "TourFeature"
        ordering = ["tour", "day"]

    def __str__(self):
        return f"{self.day}: {self.title}"
