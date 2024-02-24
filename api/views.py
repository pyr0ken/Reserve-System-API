from ast import Not
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework import status
from .serializers import ReservationDateSerializer, ReservationDetailSerializer, SonsTimeSerializer
from extensions.Timestep import TimeStep
from apps.reservations.models import Reservations, SonsTimes
from jalali_date import date2jalali
import json

shamsi = TimeStep()

def get_correct_datetime_format(date, time):
    try:
        correct_date = shamsi.get_correct_date(date)
        correct_time = shamsi.get_correct_time(time)
    except (ValueError, TypeError):
        raise NotFound

    return correct_date, correct_time

class GetReservationWeek(APIView):
    def get(self, request, week_number: int):

        if week_number not in [1, 2, 3, 4]:
            raise NotFound

        reservations_dates = shamsi.get_week_date_list(week_number)
        reservations_dates_dict = [{'date': date2jalali(date)} for date in reservations_dates]
        serializer = ReservationDateSerializer(reservations_dates_dict, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSonsTime(APIView):
    def get(self, request):
        sons_times = SonsTimes.objects.all()
        serializer = SonsTimeSerializer(sons_times, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class GetReservationsDetail(APIView):
    def get(self, request, reserve_date, reserve_time):
        # formatted the date & time
        date, time = get_correct_datetime_format(reserve_date, reserve_time)
        price: int

        # check the date dose not reserved.
        if Reservations.objects.filter(date__exact=date, time__exact=time).exists():
            raise NotFound('این روز رزرو شده است')

        sons_time = SonsTimes.objects.filter(time__exact=time)

        # check time is correct.
        if sons_time.exists():
            sons_time = sons_time.first()
            price = sons_time.price
        else:
            raise NotFound('زمان مورد نظر یافت نشد')

        # check reserve time is not expired.
        if sons_time.time < shamsi.now().time() and date == shamsi.now().date():
            raise NotFound('زمان مورد نظر گذشته است')

        # check the date is correct.
        if date < shamsi.now().date() or date > shamsi.get_week_date_list(4)[-1]:
            raise NotFound('تاریخ مورد نظر گذشته است')

        reserve_detail_dict = [
            {
                'date': date2jalali(date),
                'time': time,
                'price': price,
            }
        ]
        serializer = ReservationDetailSerializer(reserve_detail_dict, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)