from django.contrib.gis.geos import Point
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.gis.db.models import PointField
from core.models import BaseModel


class Location(BaseModel):
    name = models.CharField(_("Name"), unique=True, max_length=256)

    class Meta:
        app_label = "locations"
        ordering = ["name"]
        abstract = True

    def __str__(self):
        return self.name


class Continent(Location):
    class Meta(Location.Meta):
        verbose_name_plural = "Continents"


class Country(Location):
    continent = models.ForeignKey(
        Continent, related_name="countries", on_delete=models.CASCADE
    )
    description = models.CharField(
        _("Description"), max_length=512, null=True, blank=True
    )

    class Meta(Location.Meta):
        verbose_name_plural = "Countries"


class Destination(Location):
    # TODO: in future remove null=true blank=true
    location = PointField(
        geography=True, default=Point(27.56, 53.9), null=True, blank=True
    )
    country = models.ForeignKey(
        Country, related_name="cities", on_delete=models.CASCADE
    )

    @property
    def longitude(self):
        return self.location.x

    @property
    def latitude(self):
        return self.location.y

    class Meta(Location.Meta):
        verbose_name_plural = "Destinations"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "country"], name="uq_city_destination"
            )
        ]


class City(Destination):
    class Meta(Location.Meta):
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.pk} {self.name}, {self.country.name}"


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
