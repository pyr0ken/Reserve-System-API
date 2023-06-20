from django.contrib import admin
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
    list_display = ["user", "is_paid", "date", "time", "price"]
    list_display_links = ["user"]
    list_filter = ["date", "time", "price"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        ("Personal info", {"fields": ["user"]}),
        ("Reserve info", {"fields": ["date", "time", "price", "sons_time"]}),
        ("Transaction info", {"fields": ["is_paid", "RefID", "authority", "created_at", "updated_at"]}),
    ]
    search_fields = ["date", "time", "price", "authority", "RfID"]
    ordering = ["-date"]
    filter_horizontal = []


admin.site.register(SonsTimes, SonsTimesAdmin)
admin.site.register(Reservations, ReservationsAdmin)
