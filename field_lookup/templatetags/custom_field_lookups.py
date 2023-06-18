from django import template
from extensions.Timestap import TimeStap

register = template.Library()


@register.filter(name='three_digits_currency')
def three_digits_currency(value: int) -> str:
    return '{:,}'.format(value) + ' تومان'

# (: ببین پسر تو یه نابغه ای


@register.filter(name='get_parsian_weekday')
def get_parsian_weekday(date) -> str:
    shamsi = TimeStap()
    return shamsi.get_persian_weekday(date)
