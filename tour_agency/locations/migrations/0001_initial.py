# Generated by Django 4.0.5 on 2022-06-09 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.country')),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.AddConstraint(
            model_name='city',
            constraint=models.UniqueConstraint(fields=('name', 'country'), name='uq_city_country'),
        ),
    ]
