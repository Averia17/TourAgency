# Generated by Django 4.0.5 on 2022-07-01 17:12

import core.models
import core.utils
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("locations", "0001_initial"),
        ("hotels", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MultiCityTour",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "title",
                    models.CharField(max_length=256, unique=True, verbose_name="Title"),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=512,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "start",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="From time"
                    ),
                ),
                (
                    "end",
                    models.DateTimeField(
                        default=core.utils.one_day_hence, verbose_name="End time"
                    ),
                ),
                (
                    "tour_type",
                    models.CharField(
                        choices=[
                            ("LAND", "Land Tour"),
                            ("RIVER", "River Cruises"),
                            ("SMALL_SHIP", "Small Ship Cruises"),
                            ("FAMILY", "Family Journeys"),
                        ],
                        default="LAND",
                        max_length=10,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Price"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "MultiCityTours",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TourFeature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(auto_now=True, db_index=True)),
                ("title", models.CharField(max_length=256, verbose_name="Title")),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=512,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                ("day", models.PositiveSmallIntegerField()),
                (
                    "food",
                    core.models.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("BREAKFAST", "Breakfast"),
                                ("BRUNCH", "Brunch"),
                                ("LUNCH", "Lunch"),
                                ("SUPPER", "Supper"),
                                ("DINNER", "Dinner"),
                            ],
                            default="BREAKFAST",
                            max_length=10,
                        ),
                        size=None,
                    ),
                ),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tour_features",
                        to="locations.destination",
                    ),
                ),
                (
                    "hotel",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="tour_features",
                        to="hotels.hotel",
                    ),
                ),
                (
                    "tour",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tour_features",
                        to="tours.multicitytour",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "TourFeature",
                "ordering": ["tour", "day"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OneCityTour",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "title",
                    models.CharField(max_length=256, unique=True, verbose_name="Title"),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=512,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "start",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="From time"
                    ),
                ),
                (
                    "end",
                    models.DateTimeField(
                        default=core.utils.one_day_hence, verbose_name="End time"
                    ),
                ),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="one_city_tours",
                        to="locations.destination",
                    ),
                ),
                (
                    "hotel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="one_city_tours",
                        to="hotels.hotel",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "OneCityTours",
                "abstract": False,
            },
        ),
    ]
