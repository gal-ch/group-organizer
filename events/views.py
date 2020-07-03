from django.contrib.auth.models import Group
from rest_framework import permissions, authentication, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.generic import CreateView, UpdateView
from rest_framework.views import APIView
from events.forms import EventForm
from events.models import Event
from django.http import JsonResponse, Http404
import datetime
from django.utils import timezone
from events.serializers import EventSerializer
from django.contrib.auth import get_user_model
import datetime
User = get_user_model()


@permission_classes((permissions.AllowAny,))
class EventsList(APIView):
    """
    List all event, or create a new event.
    """
    def get(self, request, format=None):
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['user'] = request.user.pk
        data = request.data
        current_tz = timezone.get_current_timezone()
        date_start_string = '{} {}'.format(data['date'], data['start_hour'])
        date_end_string = '{} {}'.format(data['date'], data['end_hour'])
        start_t = datetime.datetime.strptime(date_start_string, "%Y-%m-%d %H:%M:%S")
        end_t = datetime.datetime.strptime(date_end_string, "%Y-%m-%d %H:%M:%S")
        data['start'] = current_tz.localize(start_t)
        data['end'] = current_tz.localize(end_t)
        serializer = EventSerializer(data=data)
        group_id = data['group_id']
        group_obj = Group.objects.get(id=group_id)
        if serializer.is_valid():
            serializer.save()
            new_event = serializer.instance
            group_obj.events.add(new_event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,))
class EventDetail(APIView):
    """
    Retrieve, update or delete a event instance.
    """
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        print('serializer', serializer.data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        data = request.data
        event = self.get_object(pk)
        data['user'] = request.user.pk
        current_tz = timezone.get_current_timezone()
        date_start_string = '{} {}'.format(data['date'], data['start_hour'])
        date_end_string = '{} {}'.format(data['date'], data['end_hour'])
        start_t = datetime.datetime.strptime(date_start_string, "%Y-%m-%d %H:%M:%S")
        end_t = datetime.datetime.strptime(date_end_string, "%Y-%m-%d %H:%M:%S")
        data['start'] = current_tz.localize(start_t)
        data['end'] = current_tz.localize(end_t)
        serializer = EventSerializer(event, data=data)
        if serializer.is_valid():
            serializer.save()
            print('putserializer', serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def event_change_date(request):
    event_id = request.GET.get('event_id')
    event_obj = Event.objects.get(id=event_id)
    if event_obj is not None:
        new_date_start = request.GET.get('new_date_start')
        new_date_end = request.GET.get('new_date_end')
        event_obj.start_time = new_date_start
        event_obj.end_time = new_date_end
        event_obj.save()
        return JsonResponse({'success': 'success'}, status=200)
    return JsonResponse({"error": ""}, status=400)


@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
def event_update_users(request, pk):
    event = Event.objects.get(id=pk)
    response = event.check_if(request.user.pk)
    print(response)
    return Response(response)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def update_event_source(request, pk):
    user = request.user.pk
    current_group = Group.objects.get(id=pk)
    events_source = {'group_id': current_group.pk, 'color': current_group.color, 'group_events': [{
        'id': o.id, 'title': o.title, 'description': o.description, 'start': o.start.isoformat(),
        'end': o.end.isoformat(), 'allDay': True, 'take_on_event': o.take_on_event, 'charge_num': o.charge_num,
        'user_id': o.user_id, 'date': o.date, 'charge_users': [u.username for u in o.charge_users.all()]} for o in current_group.events.all()]}
    print(events_source)
    return Response(events_source)
