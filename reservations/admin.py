from django.contrib import admin
from .models import SonsTimes


class SonsTimesAdmin(admin.ModelAdmin):
    list_display = ['time_format', 'price', 'holiday_price']

    def time_format(self, obj):
        return (obj.time).strftime("%H:%M:%S")
    time_format.short_description = "time"


admin.site.register(SonsTimes, SonsTimesAdmin)
