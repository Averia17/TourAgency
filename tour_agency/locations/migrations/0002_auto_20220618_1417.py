# Generated by Django 4.0.5 on 2022-06-18 14:17
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0001_initial"),
    ]

    operations = [
        CreateExtension("postgis"),
        CreateExtension("postgis_topology"),
    ]
