from django import forms


class ReservationCountForm(forms.Form):
    count = forms.IntegerField()