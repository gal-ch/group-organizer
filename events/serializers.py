from rest_framework import serializers
from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'start_time', 'end_time', 'description', 'user', 'take_on_event', 'charge_num', 'charge_users',]

