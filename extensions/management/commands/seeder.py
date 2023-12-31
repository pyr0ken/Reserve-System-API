import datetime
from django.core.management.base import BaseCommand
from apps.reservations.models import SonsTimes


class Command(BaseCommand):
    help = "add some fake data :)"

    def handle(self, *args, **options):

        SonsTimes.objects.get_or_create(time="10:00", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="12:00", price=100_000, holiday_price=200_000)
        SonsTimes.objects.get_or_create(time="15:00", price=100_000, holiday_price=200_000)

        self.stdout.write(
            self.style.SUCCESS('SonsTimes added successfully')
        )