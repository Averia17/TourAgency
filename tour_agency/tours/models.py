from django.db import models
from django.db.models import Sum, Min
from django.utils.translation import gettext_lazy as _

from core.constants import TOUR_TYPES
from core.models import BaseModel
from hotels.models import Hotel


class Tour(BaseModel):
    title = models.CharField(_("Title"), unique=True, max_length=256)
    description = models.CharField(
        _("Description"), max_length=512, null=True, blank=True
    )
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    tour_type = models.CharField(max_length=16, choices=TOUR_TYPES, default="LAND")
    max_passengers = models.PositiveSmallIntegerField(
        _("Max number of passengers"), null=True, blank=True
    )

    @property
    def days(self):
        return self.tour_features.aggregate(Sum("days"))["days__sum"]

    @property
    def min_price(self):
        hotel_price = sum(
            [
                feature.min_room_price * feature.days
                for feature in self.tour_features.filter(hotel__isnull=False).annotate(
                    min_room_price=Min("hotel__room_types__cost_per_day")
                )
            ]
        )

        return self.price + hotel_price

    @property
    def hotels(self):
        return Hotel.objects.filter(tour_features__in=self.tour_features.all())

    class Meta:
        app_label = "tours"

    def __str__(self):
        return f"{self.title}"
