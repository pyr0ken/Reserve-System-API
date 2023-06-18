from django.http import Http404
from pytz import timezone
from datetime import datetime, date, time, timedelta


class TimeStap():

    def __init__(self) -> None:
        self.TIMEZONE = timezone("Asia/Tehran")

    def now(self) -> datetime:
        return datetime.now(tz=self.TIMEZONE)

    def get_persian_weekday(self, value: date) -> str:
        days_of_week = ['دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه', 'یکشنبه']
        reserve_date = datetime.strptime(str(value), '%Y-%m-%d')
        weekday = reserve_date.weekday()
        weekday_name = days_of_week[weekday]
        return weekday_name

    def get_correct_date(self, value: str) -> date:
        return datetime.strptime(value, "%Y-%m-%d").date()

    def get_correct_time(self, value: str) -> time:
        return datetime.strptime(value, "%H:%M").time()

    def get_week_date_list(self, week_number: int) -> list[date]:
        week_date_list = []

        if not 0 < week_number < 5:
            raise Http404

        today = self.now()

        start_date = today.date() + timedelta(days=7 * (week_number - 1))
        end_date = start_date + timedelta(days=6)

        for i in range(int((end_date - start_date).days) + 1):
            week_date_list.append((start_date + timedelta(days=i)))

        return week_date_list
