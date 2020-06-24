from django import forms
from django.forms import ModelForm, DateInput, TimeInput
from events.models import Event
import datetime as dt
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]


class EventForm(ModelForm):
    start_hour = forms.ChoiceField(widget=forms.Select, choices=HOUR_CHOICES)
    end_hour = forms.ChoiceField(widget=forms.Select, choices=HOUR_CHOICES)

    class Meta:
        model = Event
        exclude = ('user', 'start_time', 'end_time', 'charge_users',)
        # widgets ={
        #     'charge_num': forms.IntegerField(required=False, widget=forms.TextInput(
        #      attrs={'type': 'number', 'min': '0', 'max':'10', 'step':'1'}))
        # }





