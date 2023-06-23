from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from extensions.Timestep import TimeStep
from .models import SonsTimes, Reservations
from .forms import ReservationCountForm
from .zarinpal import payment_request, payment_verification, ZarinpalError


class HomeView(TemplateView):
    template_name = 'reservations/home.html'


def get_correct_datetime_format(date, time):
    shamsi = TimeStep()
    try:
        correct_date = shamsi.get_correct_date(date)
        correct_time = shamsi.get_correct_time(time)
    except (ValueError, TypeError):
        raise Http404

    return correct_date, correct_time


class ReservationsTableView(View):
    shamsi = TimeStep()
    template_name = 'reservations/reserve_table.html'

    def get(self, request: HttpRequest, week_number: int):
        now = self.shamsi.now()
        week_date_list = self.shamsi.get_week_date_list(week_number)
        sons_times = SonsTimes.objects.all()

        context = {
            'now': now,
            'week_number': week_number,
            'week_dates': week_date_list,
            'sons_times': sons_times,
        }

        return render(request, self.template_name, context)


class ReservationsDetailView(View):
    shamsi = TimeStep()
    template_name = "reservations/reserve_pay.html"
    form_class = ReservationCountForm()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "لطفا اول ثبت نام کنید!")
            return redirect(reverse('reservations:table', args=[1]))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, reserve_date, reserve_time):
        # formatted the date & time
        date, time = get_correct_datetime_format(reserve_date, reserve_time)
        price: int

        # check the date dose not reserved.
        if Reservations.objects.filter(date__exact=date, time__exact=time, is_paid=True).exists():
            raise Http404

        sons_time = SonsTimes.objects.filter(time__exact=time)

        # check time is correct.
        if sons_time.exists():
            sons_time = sons_time.first()
            price = sons_time.price
        else:
            raise Http404

        # check reserve time is not expired.
        if sons_time.time < self.shamsi.now().time() and date == self.shamsi.now().date():
            raise Http404

        # check the date is correct.
        if date < self.shamsi.now().date() or date > self.shamsi.get_week_date_list(4)[-1]:
            raise Http404

        # add data to session
        request.session["reserve_data"] = {
            "date": f"{date}",
            "time": f"{time}",
        }

        context = {
            "form": self.form_class,
            "reserve_date": date,
            "reserve_time": time,
            "reserve_price": price,
        }

        return render(request, self.template_name, context)


class ReservationsPaymentView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        reserve_count = request.POST.get("count")
        reserve_data = request.session["reserve_data"]

        reserve_date = reserve_data.get("date")
        reserve_time = reserve_data.get("time")

        date, time = get_correct_datetime_format(reserve_date, reserve_time)
        sons_time = SonsTimes.objects.filter(time__exact=time).first()
        price = sons_time.price

        try:
            count = int(reserve_count)
        except ValueError:
            raise Http404

        if not 1 <= count <= 50:
            raise Http404

        print(reserve_count)
        print(count)

        add_reserve = Reservations(
            user_id=request.user.id,
            sons_time_id=sons_time.id,
            date=date,
            time=time,
            price=price,
            count=count,
        )

        amount = int(add_reserve.price * count)  # * 10 for convert to Rial
        description = "! Thank You Man"
        phone_number = add_reserve.user.phone_number
        try:
            redirect_url = payment_request(amount, description, add_reserve, phone_number)
            return redirect(redirect_url)

        except ZarinpalError as e:
            return HttpResponse(e)


class ReservationsVerifyView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):

        if request.GET.get('Status') == 'OK':
            authority = int(request.GET.get('Authority'))
            try:
                # try to found transaction
                try:
                    add_reserve = Reservations.objects.get(authority=authority)

                # if we couldn't find the transaction
                except ObjectDoesNotExist:
                    return HttpResponse('we can\'t find this transaction')
                except MultipleObjectsReturned:
                    raise Http404

                price = int(add_reserve.price * add_reserve.count)  # * 10 for convert to Rial.
                code, message, ref_id = payment_verification(price, authority)

                # everything is ok
                if code == 100:
                    count = add_reserve.count
                    print(count)

                    # todo: fix date validator bug.
                    for reserve_count in range(0, count):

                        new_reservation_date = add_reserve.date + timedelta(days=7 * reserve_count)

                        while Reservations.objects.filter(date__exact=new_reservation_date, is_paid=True).exists():
                            new_reservation_date += timedelta(days=7)

                        new_reserve = Reservations(
                            user_id=add_reserve.user.id,
                            sons_time_id=add_reserve.sons_time.id,
                            time=add_reserve.time,
                            price=add_reserve.price,
                            authority=add_reserve.authority,
                            count=add_reserve.count,
                            RefID=ref_id,
                            is_paid=True,
                            date=new_reservation_date,
                        )
                        new_reserve.save()

                    Reservations.objects.get(authority=authority, is_paid=False).delete()

                    content = {
                        'type': 'Success',
                        'ref_id': ref_id
                    }
                    # messages.success(request, f'پرداخت با موفیقت انجام شد. کد رهگیری {ref_id}')
                    return HttpResponse("<h1>Success!</h1>")


                # operation was successful but PaymentVerification operation on this transaction have already been done
                elif code == 101:
                    content = {
                        'type': 'Warning'
                    }
                    # messages.error(request, f'پرداخت با خطا مواجه شد.')
                    return HttpResponse("<h1>Error!</h1>")

            # if got an error from zarinpal
            except ZarinpalError as e:
                return HttpResponse(e)

        # messages.error(request, f'پرداخت با خطا مواجه شد.')
        return HttpResponse("<h1>Error!</h1>")
