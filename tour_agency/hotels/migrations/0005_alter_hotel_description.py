# Generated by Django 4.0.5 on 2022-07-19 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_remove_roomtype_count_rooms_alter_roomtype_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='description',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Description'),
        ),
    ]
