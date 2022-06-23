from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.constants import TOUR_TYPES, MEALS
from core.models import BaseModel, ChoiceArrayField
from core.utils import one_day_hence
from hotels.models import Hotel
from locations.models import City


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
    city = models.ForeignKey(
        City, related_name="one_city_tours", on_delete=models.CASCADE
    )

    class Meta(Tour.Meta):
        verbose_name_plural = "OneWayTours"


class MultiCityTour(BaseModel, Tour):
    tour_type = models.CharField(max_length=10, choices=TOUR_TYPES, default="LAND")
    start = models.DateTimeField(_("From time"), default=timezone.now)
    end = models.DateTimeField(_("End time"), default=one_day_hence)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)

    class Meta(Tour.Meta):
        verbose_name_plural = "MultiWaysTours"


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
        Hotel, related_name="tour_features", on_delete=models.SET_NULL, null=True
    )
    city = models.ForeignKey(
        City, related_name="tour_features", on_delete=models.CASCADE
    )
    tour = models.ForeignKey(
        MultiCityTour, related_name="tour_features", on_delete=models.CASCADE
    )

    class Meta(Tour.Meta):
        app_label = "tours"
        verbose_name_plural = "TourFeature"
        ordering = ["day"]

    def __str__(self):
        return f"{self.day}: {self.title}"
