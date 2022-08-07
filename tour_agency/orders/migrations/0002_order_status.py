# Generated by Django 4.0.5 on 2022-08-05 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('SUCCESS', 'Success'), ('PENDING_PAYMENT', 'Pending payment'), ('BOOKED', 'Booked'), ('FAULT', 'Fault'), ('CANCELED', 'Canceled')], default='BOOKED', max_length=15, verbose_name='Status'),
        ),
    ]
