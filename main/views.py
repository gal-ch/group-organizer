from django.conf import settings
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views import generic
from events.forms import EventForm
from events.models import Event
from django.contrib.auth import get_user_model
User = get_user_model()


class CalendarView(generic.DetailView):
    model = Group
    template_name = 'main/calendar.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        ''' checks if the user is logged in and a member in the current group -
        if not he will be redirected to login page or his group calendar 
        and if he is not member of any he will be redirect to create a group '''
        if user.is_authenticated:
            try:
                self.get_object().user_set.get(id=user.pk)
            except:
                if user.groups.first() is not None:
                    return HttpResponseRedirect('main:calendar', kwargs={'pk': user.groups.first().id})
                else:
                    return HttpResponseRedirect('create-group')
            return super(CalendarView, self).dispatch(request, *args, **kwargs)
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        '''get the event related to current group'''
        user = self.request.user
        events_group = self.object.events.all()
        context['events'] = [{'id': o.id, 'title': o.title, 'description': o.description,
                              'start': o.start_time.isoformat(), 'end': o.end_time.isoformat(),
                              'allDay': True, 'to_do': o.take_on_event, 'charge_num': o.charge_num,
                              'user_id': o.user_id} for o in events_group]
        context['users_in_group'] = self.object.user_set.all()
        context['user_groups'] = Group.objects.filter(user=user)
        context['manger_perm'] = user.has_perm('auth.change_group')
        context['eventForm'] = EventForm()
        return context


def get_charge_users(request):
    event_obj = Event.objects.get(id=request.GET.get('event_id'))
    users_list = event_obj.get_charge_users()
    print(users_list)
    response_data = {'users_list': users_list}
    return JsonResponse(response_data)










