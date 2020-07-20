from rest_framework import serializers
from events.models import Event
# not using


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id',
                  'date',
                  'title',
                  'start',
                  'end',
                  'description',
                  'user',
                  'take_on_event',
                  'charge_num',
                  ]

    def create(self, validated_data):
        """
        Create and return a new `Event` instance, given the validated data.
        """
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.charge_num = validated_data.get('charge_num', instance.charge_num)
        instance.date = validated_data.get('date', instance.date)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.take_on_event = validated_data.get('take_on_event', instance.take_on_event)
        instance.save()
        return instance


