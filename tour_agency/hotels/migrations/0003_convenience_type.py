# Generated by Django 4.0.5 on 2022-07-01 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='convenience',
            name='type',
            field=models.CharField(choices=[('HOTEL', 'Hotel'), ('ROOM', 'Room')], default='HOTEL', max_length=16, verbose_name='Type'),
        ),
    ]