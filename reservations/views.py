from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import Http404, JsonResponse, HttpRequest, HttpResponseRedirect, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from datetime import timedelta
from extensions.Timestap import TimeStap
from .models import SonsTimes
from .serializers import SonsTimeSerializers


class ReservationsAPIView(APIView):
    def get(self, request, week_number):

        if not 0 < week_number < 5:
            raise NotFound("Week number not found")

        shamsi = TimeStap()
        today = shamsi.now()

        start_date = today.date() + timedelta(days=7 * (week_number - 1))
        end_date = start_date + timedelta(days=6)

        week_date_list = []

        for i in range(int((end_date - start_date).days) + 1):
            week_date_list.append((start_date + timedelta(days=i)))

        week_date_weekday_list = []

        for date in week_date_list:
            week_date_weekday_list.append(shamsi.get_persian_weekday(date))

        sons_times = SonsTimes.objects.all()
        serializer = SonsTimeSerializers(sons_times, many=True)

        context = {
            'week_date': week_date_list,
            'week_date_weekday': week_date_weekday_list,
            'sons_times': serializer.data,
        }

        return Response(context, status=status.HTTP_200_OK)


def is_valid_reservation(week_number, date, time, price):
    shamsi = TimeStap()

    # Convert data to current format.
    try:
        current_date = shamsi.get_correct_date(date)
        current_time = shamsi.get_correct_time(time)
        current_price = int(price)
        current_week_number = int(week_number)
    except (ValueError, TypeError):
        # todo: set a error message.
        raise Response("ValueError or TypeError")

    week_date_list = shamsi.get_week_date_list(current_week_number)

    # Validator for date, time, price.
    if current_date not in week_date_list or not SonsTimes.objects.filter(time__exact=current_time,
                                                                          price__exact=current_price).exists():
        # todo: set a error message.
        raise Response("Reservations NotFond")

    return current_date, current_time, current_price, current_week_number


class ReservationsView(View):
    shamsi = TimeStap()
    template_name = 'reservations/reserve.html'

    def get(self, request: HttpRequest, week_number: int):
        sons_times = SonsTimes.objects.all()
        week_date_list = self.shamsi.get_week_date_list(week_number)
        now_time = self.shamsi.now().time()

        context = {
            'now_time': now_time,
            'week_number': week_number,
            'week_date': week_date_list,
            'sons_times': sons_times,
        }

        return render(request, self.template_name, context)


class PaymentView(View):
    template_name = 'reservations/payment.html'
    shamsi = TimeStap()

    def get(self, request, *args, **kwargs):
        date = request.GET.get('date')
        time = request.GET.get('time')
        price = request.GET.get('price')
        week_number = request.GET.get('week')

        formatted_date, formatted_time, formatted_price, formatted_week_number = is_valid_reservation(week_number, date,
                                                                                                      time, price)

        print("==GET==" * 90)
        print(formatted_date, type(formatted_date))
        print(formatted_time, type(formatted_time))
        print(formatted_price, type(formatted_price))
        print(formatted_week_number, type(formatted_week_number))

        context = {
            'date': formatted_date,
            'time': formatted_time,
            'price': formatted_price,
            'week_number': formatted_week_number,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        date = request.POST.get("date")
        time = request.POST.get("time")
        price = request.POST.get("price")
        week_number = request.POST.get("week")

        print(date, time, price, week_number)

        formatted_date, formatted_time, formatted_price, formatted_week_number = is_valid_reservation(week_number, date,
                                                                                                      time, price)

        print("==POST=="*90)
        print(formatted_date, type(formatted_date))
        print(formatted_time, type(formatted_time))
        print(formatted_price, type(formatted_price))
        print(formatted_week_number, type(formatted_week_number))

        return redirect(reverse('reservations:table', args=[formatted_week_number]))
