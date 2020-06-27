from django.conf import settings
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from events.forms import EventForm
from events.models import Event
from django.contrib.auth import get_user_model
User = get_user_model()


class CalendarView(generic.DetailView):
    model = User
    template_name = 'main/calendar.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        print(user.pk)
        ''' checks if the user is logged in and a member in the current group -
        if not he will be redirected to login page or his group calendar
        and if he is not member of any he will be redirect to create a group '''
        if user.is_authenticated:
            return super(CalendarView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        '''get the event related to current group'''

        user_groups = Group.objects.filter(user=self.object)

        context['events'] = [{'group_id': group.pk, 'group_events': [{'id': o.id, 'title': o.title, 'description': o.description,
                              'start': o.start_time.isoformat(), 'end': o.end_time.isoformat(),
                              'allDay': True, 'to_do': o.take_on_event, 'charge_num': o.charge_num,
                              'user_id': o.user_id} for o in group.events.all()]} for group in user_groups]
        context['user_groups'] = Group.objects.filter(user=self.object)
        context['manger_perm'] = self.object.has_perm('auth.change_group')
        context['eventForm'] = EventForm()
        return context


def get_charge_users(request):
    event_obj = Event.objects.get(id=request.GET.get('event_id'))
    users_list = event_obj.get_charge_users()
    print(users_list)
    response_data = {'users_list': users_list}
    return JsonResponse(response_data)










