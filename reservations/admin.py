from django.contrib import admin
from django.db import models
from django.db.models import Q
from jalali_date import date2jalali
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from jdatetime import date as jdatetime_date
from jdatetime import datetime as jdatetime_datetime

from .models import SonsTimes, Reservations


class SonsTimesAdmin(admin.ModelAdmin):
    list_display = ['time_format', 'price', 'holiday_price']
    list_display_links = ["time_format"]
    fieldsets = [
        ("Time info", {"fields": ["time"]}),
        ("Price info", {"fields": ["price", "holiday_price"]}),
    ]

    def time_format(self, obj):
        return (obj.time).strftime("%H:%M:%S")

    time_format.short_description = "time"


class ReservationsAdmin(admin.ModelAdmin):
    list_display = ["user", "is_paid", "jdate", "time_format", "price"]
    list_display_links = ["user"]
    list_filter = ["is_paid", "date", "time", "price"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        ("Personal info", {"fields": ["user"]}),
        ("Reserve info", {"fields": ["date", "time", "price", "sons_time", "count"]}),
        ("Transaction info", {"fields": ["is_paid", "RefID", "authority", "created_at", "updated_at"]}),
    ]
    search_fields = ["date", "time", "price", "authority", "RfID"]
    ordering = ["date", "time"]
    filter_horizontal = []

    # formfield_overrides = {
    #     models.DateField: {
    #         'form_class': JalaliDateField,
    #         'widget': AdminJalaliDateWidget,
    #     },
    # }

    def jdate(self, obj):
        return date2jalali(obj.date).strftime("%Y / %m/ %d")

    jdate.short_description = "date"

    def time_format(self, obj):
        return (obj.time).strftime("%H:%M:%S")

    time_format.short_description = "time"


admin.site.register(SonsTimes, SonsTimesAdmin)
admin.site.register(Reservations, ReservationsAdmin)
