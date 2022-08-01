from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone


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
