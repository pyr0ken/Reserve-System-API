import datetime

from django import template
from extensions.Timestap import TimeStap
from reservations.models import Reservations

register = template.Library()


@register.filter(name='three_digits_currency')
def three_digits_currency(value: int) -> str:
    return '{:,}'.format(value) + ' تومان'


@register.filter(name='get_persian_weekday')
def get_persian_weekday(date) -> str:
    shamsi = TimeStap()
    return shamsi.get_persian_weekday(date)


@register.filter(name="check_reserved_date")
def check_reserved_date(date: datetime.date) -> bool:
    if Reservations.objects.filter(date__exact=date, is_paid=True).exists():
        return True


@register.filter(name="check_reserved_time")
def check_reserved_time(time: datetime.time) -> bool:
    if Reservations.objects.filter(time__exact=time, is_paid=True).exists():
        return True


@register.simple_tag(name="get_fullname_reserved_date")
def get_fullname_reserved_date(date: datetime.date, time: datetime.time) -> str:
    reserved_data = Reservations.objects.filter(date__exact=date, time__exact=time, is_paid=True).first()
    return reserved_data.user

