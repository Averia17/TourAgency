from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from core.constants import TOUR_TYPES, MEALS
from core.models import BaseModel, ChoiceArrayField
from hotels.models import Hotel
from locations.models import City, Destination


class Tour(BaseModel):
    title = models.CharField(_("Title"), unique=True, max_length=256)
    description = models.CharField(
        _("Description"), max_length=512, null=True, blank=True
    )
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    tour_type = models.CharField(max_length=16, choices=TOUR_TYPES, default="LAND")

    @property
    def days(self):
        return self.tour_features.aggregate(Sum("days"))["days__sum"]

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

    @property
    def hotels(self):
        return Hotel.objects.filter(tour_features__in=self.tour_features.all())

    class Meta:
        app_label = "tours"

    def __str__(self):
        return f"{self.title}"


class TourFeature(BaseModel):
    title = models.CharField(_("Title"), max_length=256)
    description = models.CharField(
        _("Description"), max_length=1024, null=True, blank=True
    )
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
        order_with_respect_to = "tour"

    def __str__(self):
        return f"{self.days}: {self.title}"
