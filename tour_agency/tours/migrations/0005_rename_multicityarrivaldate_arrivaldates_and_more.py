# Generated by Django 4.0.5 on 2022-07-19 10:57

from django.db import migrations, models


def set_tour_features_order(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    TourFeature = apps.get_model("tours", "TourFeature")
    features = []
    for tour in Tour.objects.all().prefetch_related("tour_features"):
        print(tour)
        for index, feature in enumerate(tour.tour_features.all(), start=1):
            feature.order = index
            features.append(feature)
    TourFeature.objects.bulk_update(features, ["order"])


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0002_rename_multicitytourimage_tourimage_and_more"),
        ("tours", "0004_onecitytour_price"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="MultiCityArrivalDate",
            new_name="ArrivalDates",
        ),
        migrations.RenameModel(
            old_name="MultiCityTour",
            new_name="Tour",
        ),
        migrations.RemoveField(
            model_name="onecityarrivaldate",
            name="tour",
        ),
        migrations.RemoveField(
            model_name="onecitytour",
            name="destination",
        ),
        migrations.RemoveField(
            model_name="onecitytour",
            name="hotel",
        ),
        migrations.AlterModelOptions(
            name="arrivaldates",
            options={"verbose_name_plural": "ArrivalDates"},
        ),
        migrations.AlterModelOptions(
            name="tour",
            options={},
        ),
        migrations.AlterModelOptions(
            name="tourfeature",
            options={
                "get_latest_by": ["order"],
                "ordering": ["tour", "order"],
                "verbose_name_plural": "TourFeature",
            },
        ),
        migrations.RemoveField(
            model_name="tourfeature",
            name="day",
        ),
        migrations.AddField(
            model_name="tourfeature",
            name="days",
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="tourfeature",
            name="order",
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.RunPython(
            set_tour_features_order, reverse_code=migrations.RunPython.noop
        ),
        migrations.AddConstraint(
            model_name="tourfeature",
            constraint=models.UniqueConstraint(
                fields=("tour", "order"), name="uq_tour_order"
            ),
        ),
        migrations.DeleteModel(
            name="OneCityArrivalDate",
        ),
        migrations.DeleteModel(
            name="OneCityTour",
        ),
    ]
