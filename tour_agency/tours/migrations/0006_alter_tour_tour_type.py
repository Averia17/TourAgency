# Generated by Django 4.0.5 on 2022-07-19 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0005_rename_multicityarrivaldate_arrivaldates_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tour",
            name="tour_type",
            field=models.CharField(
                choices=[
                    ("LAND", "Land Tour"),
                    ("ONE_DESTINATION", "One Destination Journey"),
                    ("RIVER", "River Cruises"),
                    ("SMALL_SHIP", "Small Ship Cruises"),
                    ("FAMILY", "Family Journeys"),
                ],
                default="LAND",
                max_length=16,
            ),
        ),
    ]