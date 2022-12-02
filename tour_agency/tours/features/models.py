from django.db import models
from django.utils.translation import gettext_lazy as _

from hotels.models import Hotel
from locations.models import Destination
from core.constants import MEALS
from core.models import BaseModel, ChoiceArrayField
from tours.models import Tour


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
