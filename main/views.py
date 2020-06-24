from django.http import JsonResponse
from django.views import generic
from events.forms import EventForm
from events.models import Event
from django.contrib.auth import get_user_model
User = get_user_model()


class CalendarView(generic.ListView):
    model = Event
    template_name = 'main/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eventForm'] = EventForm()
        events = Event.objects.all()
        context['events'] = [{'id': o.id, 'title': o.title, 'description': o.description,
                              'start': o.start_time.isoformat(), 'end': o.end_time.isoformat(),
                              'allDay': True, 'to_do': o.take_on_event, 'charge_num': o.charge_num,
                              'user_id': o.user_id} for o in events]
        context['users_in_group'] = User.objects.all()
        context['user'] = self.request.user
        return context


def get_charge_users(request):
    event_obj = Event.objects.get(id=request.GET.get('event_id'))
    users_list = event_obj.get_charge_users()
    print(users_list)
    response_data = {'users_list': users_list}
    return JsonResponse(response_data)


def user_to_charge_list(request):
    check_user = Event.objects.get(id=request.GET.get('event_id')).check_if(request.user.pk)
    data = {'check_user': check_user, 'name': request.user.username}
    d = User.objects.filter(event=request.GET.get('event_id'), in_charge=request.user.pk)
    return JsonResponse(data)








