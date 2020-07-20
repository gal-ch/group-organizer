from django.contrib.auth.models import Group
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from events.models import Event
from django.http import JsonResponse
from django.contrib.auth import get_user_model
User = get_user_model()


def event_change_date(request):
    event_id = request.POST.get('event_id')
    event_obj = Event.objects.get(id=event_id)
    if event_obj is not None:
        event_obj.start = request.POST.get('new_start')
        event_obj.end = request.POST.get('new_end')
        event_obj.date = request.POST.get('new_date')
        event_obj.save()
        return JsonResponse({'success': 'success'}, status=200)
    return JsonResponse({"error": ""}, status=400)


@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
def event_update_users(request, pk):
    ''' if possible, add the user to the list of users in charge for the event, and if not send an appropriate
    message to the client '''
    event = Event.objects.get(id=pk)
    response = event.check_if(request.user.pk)
    return Response(response)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def update_event_source(request, pk):
    current_group = Group.objects.get(id=pk)
    events_source = {'group_id': current_group.pk, 'color': current_group.color, 'group_events': [{
        'id': o.id, 'title': o.title, 'description': o.description, 'start': o.start.isoformat(),
        'end': o.end.isoformat(), 'allDay': True, 'take_on_event': o.take_on_event, 'charge_num': o.charge_num,
        'user_id': o.user_id, 'date': o.date, 'charge_users': [u.username for u in o.charge_users.all()]} for o in current_group.events.all()]}
    return Response(events_source)



