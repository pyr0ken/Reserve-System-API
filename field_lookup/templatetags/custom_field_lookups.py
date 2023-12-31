import datetime
from django import template
from extensions.Timestep import TimeStep
from apps.reservations.models import Reservations

register = template.Library()
shamsi = TimeStep()


@register.filter(name='three_digits_currency')
def three_digits_currency(value: int) -> str:
    return '{:,}'.format(value)


@register.filter(name='get_persian_weekday')
def get_persian_weekday(date) -> str:
    return shamsi.get_persian_weekday(date)


@register.filter(name="check_reserved_date")
def check_reserved_date(date: datetime.date, time: datetime.time) -> bool:
    if Reservations.objects.filter(date__exact=date, time__exact=time, is_paid=True).exists():
        return True


@register.filter(name="check_time_outed_date")
def check_time_outed_date(date: datetime.date, time: datetime.time) -> bool:
    if Reservations.objects.filter(date__exact=date, time__exact=time, is_paid=True).exists():
        return False
    if time < shamsi.now().time() and date == shamsi.now().date():
        return True


@register.simple_tag(name="get_fullname_reserved_date")
def get_fullname_reserved_date(date: datetime.date, time: datetime.time) -> str:
    reserved_data = Reservations.objects.filter(date__exact=date, time__exact=time, is_paid=True).first()
    full_name = f"{reserved_data.user}"
    if len(full_name) > 14:
        full_name = full_name[:14] + "..."
    return full_name


@register.simple_tag(name="check_date_status")
def check_date_status(date: datetime.date, time: datetime.time) -> str:
    date_status = 'open'
    if Reservations.objects.filter(date__exact=date, time__exact=time, is_paid=True).exists():
        date_status = 'reserved'
        return date_status
    elif date == shamsi.now().date() and time < shamsi.now().time():
        date_status = 'closed'
        return date_status
    else:
        return date_status

@register.filter(name="check_holiday_price")
def check_holiday_price(date: datetime.date):
    if shamsi.get_persian_weekday(date) in ['پنجشنبه', 'جمعه']:
        return True
    return False


@register.filter(name='datetime_to_timestamp')
def datetime_to_timestamp(date, time):
    datetime_str = f'{date} {time}'
    dt_object = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    timestamp = dt_object.timestamp()
    return int(timestamp)