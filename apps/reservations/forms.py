from django import forms


class ReservationCountForm(forms.Form):
    count = forms.IntegerField(initial=1, widget=forms.NumberInput(attrs={'type': 'range'}))
