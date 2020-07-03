from django import forms
from django.contrib.auth.models import Group
from django.forms import ModelForm, DateInput, TimeInput
from django.http import request

from events.models import Event
import datetime as dt
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]


class EventForm(ModelForm):
    start_hour = forms.ChoiceField(widget=forms.Select, choices=HOUR_CHOICES)
    end_hour = forms.ChoiceField(widget=forms.Select, choices=HOUR_CHOICES)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = Event
        exclude = ('user', 'start', 'end', 'charge_users','date')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(user=self.request.user.pk)






