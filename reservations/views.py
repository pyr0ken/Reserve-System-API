from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from extensions.Timestap import TimeStap
from .models import SonsTimes, Reservations
from .forms import ReservationCountForm
from .zarinpal import payment_request, payment_verification, ZarinpalError


def get_correct_datetime_format(date, time):
    shamsi = TimeStap()
    try:
        correct_date = shamsi.get_correct_date(date)
        correct_time = shamsi.get_correct_time(time)
    except (ValueError, TypeError):
        raise Http404

    return correct_date, correct_time


class ReservationsTableView(View):
    shamsi = TimeStap()
    template_name = 'reservations/reserve.html'

    def get(self, request: HttpRequest, week_number: int):
        now = self.shamsi.now()
        week_date_list = self.shamsi.get_week_date_list(week_number)
        sons_times = SonsTimes.objects.all()

        context = {
            'now': now,
            'week_number': week_number,
            'week_date': week_date_list,
            'sons_times': sons_times,
        }

        return render(request, self.template_name, context)


class ReservationsDetailView(View):
    shamsi = TimeStap()
    template_name = "reservations/reserve_pay.html"
    form_class = ReservationCountForm()

    def get(self, request: HttpRequest, reserve_date, reserve_time):
        # formatted the date & time
        count = request.GET.get("count")
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
            "count": f"{count}"
        }

        context = {
            "form": self.form_class,
            "date": date,
            "time": time,
            "price": price,
        }

        return render(request, self.template_name, context)


class ReservationsPaymentView(View):
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

        print(reserve_count)
        print(count)

        request.session["reserve_data"]["count"] = f"{count}"

        new_reserve = Reservations(
            user_id=request.user.id,
            sons_time_id=sons_time.id,
            date=date,
            time=time,
            price=price,
        )

        amount = int(new_reserve.price * 10)  # convert to Rial
        description = "! Thank You Man"
        email = new_reserve.user.email
        try:
            redirect_url = payment_request(amount, description, new_reserve, email)

            return HttpResponse(f"{count}")
            # return redirect(redirect_url)
        except ZarinpalError as e:
            return HttpResponse(e)


class ReservationsVerifyView(View):
    def get(self, request: HttpRequest):
        if request.GET.get('Status') == 'OK':
            authority = int(request.GET.get('Authority'))
            try:
                # try to found transaction
                try:
                    new_reserve = Reservations.objects.get(authority=authority)

                # if we couldn't find the transaction
                except ObjectDoesNotExist:
                    return HttpResponse('we can\'t find this transaction')

                code, message, ref_id = payment_verification(new_reserve.price * 10, authority)

                # everything is ok
                if code == 100:
                    count = request.session["reserve_data"]["count"]

                    new_reserve.RefID = ref_id
                    new_reserve.is_paid = True
                    new_reserve.save()

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
