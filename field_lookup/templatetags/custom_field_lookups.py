from django import template
from extensions.Timestap import TimeStap
from reservations.models import Reservations

register = template.Library()


@register.filter(name='three_digits_currency')
def three_digits_currency(value: int) -> str:
    return '{:,}'.format(value) + ' تومان'

@register.filter(name='get_parsian_weekday')
def get_parsian_weekday(date) -> str:
    shamsi = TimeStap()
    return shamsi.get_persian_weekday(date)


@register.filter(name="get_reserved_date_paid")
def get_reserved_date_paid(value: Reservations) -> Reservations:
    return value.filter(is_paid=True)