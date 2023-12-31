from sqlite3 import Time
from rest_framework import serializers
from extensions.Timestep import TimeStep

shamsi = TimeStep()

class ReservationDateSerializer(serializers.Serializer):
    date = serializers.DateField()
    day_of_week = serializers.SerializerMethodField()

    def get_day_of_week(self, obj):
        return shamsi.get_persian_weekday(obj['date'])


class ReservationDetailSerializer(serializers.Serializer):
    date = serializers.DateField()
    time = serializers.TimeField()
    price = serializers.DecimalField(decimal_places=0, max_digits=10)
    day_of_week = serializers.SerializerMethodField()

    def get_day_of_week(self, obj):
        return shamsi.get_persian_weekday(obj['date'])

