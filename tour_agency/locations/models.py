from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class Country(BaseModel):
    name = models.CharField(_("Name"), unique=True, max_length=256)

    class Meta:
        app_label = "locations"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class City(BaseModel):
    name = models.CharField(_("Name"), max_length=256)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        app_label = "locations"
        verbose_name_plural = "Cities"
        constraints = [
            models.UniqueConstraint(fields=["name", "country"], name="uq_city_country")
        ]

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class StreetMixin(models.Model):
    street = models.CharField(_("Street"), max_length=256)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=["street", "city"], name="uq_street_city")
        ]

    def get_full_name(self):
        return f"{self.street}, {str(self.city)}"
