# Generated by Django 4.0.5 on 2022-07-15 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0003_alter_tourfeature_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="onecitytour",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=10, verbose_name="Price"
            ),
            preserve_default=False,
        ),
    ]
