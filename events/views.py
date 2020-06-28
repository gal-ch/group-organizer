from django.contrib.auth.models import Group
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.generic import CreateView, UpdateView
from events.forms import EventForm
from events.models import Event
from django.http import JsonResponse
import datetime
from django.utils import timezone
from events.serializers import EventSerializer


class EventCreate(CreateView):
    form_class = EventForm
    success_url = '/calendar'

    def get_form_kwargs(self):
        kwargs = super(EventCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user.pk
        return kwargs

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            ''' 
            get event data from the client, 
            convert the time
            save the event to the data base
            add the event to the current group
            send to the client the event id and the converted start and end time of the event
            '''
            form = self.form_class(self.request.POST)
            current_tz = timezone.get_current_timezone()
            group_id = request.POST.get('current_group')
            print(group_id)
            group_obj = Group.objects.get(id=group_id)
            date_start_string = '{} {}'.format(request.POST.get('date'), request.POST.get('start_hour'))
            date_end_string = '{} {}'.format(request.POST.get('date'),  request.POST.get('end_hour'))
            start_t = datetime.datetime.strptime(date_start_string, "%Y-%m-%d %H:%M:%S")
            end_t = datetime.datetime.strptime(date_end_string, "%Y-%m-%d %H:%M:%S")
            start_date = current_tz.localize(start_t)
            end_date = current_tz.localize(end_t)
            if form.is_valid():
                new_event = form.save(commit=False)
                new_event.user_id = self.request.user.pk
                new_event.title = request.POST.get('title')
                new_event.description = request.POST.get('description')
                # print(request.POST.get('to_do'))
                # new_event.take_on_event = request.POST.get('to_do')
                new_event.charge_num = request.POST.get('charge_num')
                new_event.start_time = start_date
                new_event.end_time = end_date
                new_event = form.save(commit=True)
                group_obj.events.add(new_event)
                response = {
                    "instance_id": new_event.id,
                    "start_time": new_event.start_time,
                    "end_time": new_event.end_time,
                }
                # send to client side.
                return JsonResponse(response, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)


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


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def event_detail(request, pk):
    tasks = Event.objects.get(id=pk)
    print(tasks)
    serializer = EventSerializer(tasks, many=False)
    print(serializer)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
def event_update(request, pk):
    event = Event.objects.get(id=pk)
    response = event.check_if(request.user.pk)
    print(response)
    return Response(response)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def update_event_source(request, pk):
    user = request.user.pk
    current_group = Group.objects.get(id=pk)
    events_source = {'group_id': pk, 'group_events': [{
        'id': o.id, 'title': o.title, 'description': o.description, 'start': o.start_time.isoformat(),
        'end': o.end_time.isoformat(),'allDay': True, 'to_do': o.take_on_event, 'charge_num': o.charge_num,
        'user_id': o.user_id} for o in current_group.events.all()]}
    return Response(events_source)
