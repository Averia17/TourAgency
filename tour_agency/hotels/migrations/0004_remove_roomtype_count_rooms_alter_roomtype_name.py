# Generated by Django 4.0.5 on 2022-07-15 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0003_convenience_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="roomtype",
            name="count_rooms",
        ),
        migrations.AlterField(
            model_name="roomtype",
            name="name",
            field=models.CharField(max_length=32, verbose_name="Name"),
        ),
    ]
