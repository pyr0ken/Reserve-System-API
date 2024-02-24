import datetime
from django.core.management.base import BaseCommand
from apps.reservations.models import SonsTimes


class Command(BaseCommand):
    help = "add some fake data :)"

    def handle(self, *args, **options):

        SonsTimes.objects.get_or_create(time="01:30", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="07:30", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="09:00", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="10:30", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="12:00", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="13:30", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="15:00", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="16:30", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="18:00", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="19:30", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="21:00", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="22:30", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="23:59", price=100_000, holiday_price=200_000)

        self.stdout.write(
            self.style.SUCCESS('SonsTimes added successfully')
        )