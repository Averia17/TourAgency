# Generated by Django 4.0.5 on 2022-08-19 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="count_persons",
            field=models.PositiveSmallIntegerField(
                default=1, verbose_name="Count Persons"
            ),
            preserve_default=False,
        ),
    ]
