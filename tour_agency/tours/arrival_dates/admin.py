from django.contrib import admin

from tours.arrival_dates.models import ArrivalDates


class ArrivalDateInline(admin.TabularInline):
    model = ArrivalDates
    extra = 1
