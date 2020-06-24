from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from events.forms import EventForm
from events.models import Event
from django.http import JsonResponse
import datetime
from django.utils import timezone


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('main:calendar'))
    return render(request, 'events/event.html', {'form': form})


class EventCreate(CreateView):
    form_class = EventForm
    success_url = '/calendar'

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            ''' 
            get event data from the client, 
            convert the time
            save the event to the data base
            send to the client the event id and the converted start and end time of the event
            '''
            form = self.form_class(self.request.POST)
            current_tz = timezone.get_current_timezone()
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


def update_event(request):
    print(request.GET.get('event_id'))


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
