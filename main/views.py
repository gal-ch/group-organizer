import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import Group
from accounts.models import FriendRequest, Friendship
from events.forms import EventForm
from events.models import Event
from django.contrib.auth import get_user_model
User = get_user_model()


class CalendarView(FormMixin, ListView):
    model = User
    template_name = 'main/calendar.html'
    form_class = EventForm

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        ''' checks if the user is logged in and a member in the current group -
        if not he will be redirected to login page or his group calendar
        and if he is not member of any he will be redirect to create a group '''
        if user.is_authenticated:
            return super(CalendarView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def get_form_kwargs(self):
        kwargs = super(CalendarView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_queryset(self):
        user = self.request.user
        user_groups_qs = user.groups.all()
        return user_groups_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        '''get the event related to current user'''
        user = self.request.user
        context['events'] = [
            {'group_id': group.pk, 'group_events': [{'id': o.id, 'title': o.title, 'description': o.description,
                                                     'start': o.start.isoformat(), 'end': o.end.isoformat(),
                                                     'allDay': True, 'take_on_event': o.take_on_event, 'date': o.date,
                                                     'charge_num': o.charge_num,
                                                     'user_id': o.user_id} for o in group.events.all()]} for group in
            self.get_queryset()]
        context['manger_perm'] = user.has_perm('auth.change_group')
        context['user_friends'] = Friendship.objects.friends_of(user=self.request.user)
        context['user_friends_request'] = FriendRequest.objects.filter(receiver=user)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        '''
        get event data from the client,
        convert the time
        save the event to the data base
        add the event to the selected group
        send to the client the event id and the converted start and end time of the event
        '''
        current_tz = timezone.get_current_timezone()
        group_id = self.request.POST.get('current_group')
        group_obj = Group.objects.get(id=group_id)
        date_start_string = '{} {}'.format(self.request.POST.get('date'), self.request.POST.get('start_hour'))
        date_end_string = '{} {}'.format(self.request.POST.get('date'), self.request.POST.get('end_hour'))
        start_t = datetime.datetime.strptime(date_start_string, "%Y-%m-%d %H:%M:%S")
        end_t = datetime.datetime.strptime(date_end_string, "%Y-%m-%d %H:%M:%S")
        start_date = current_tz.localize(start_t)
        end_date = current_tz.localize(end_t)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.user_id = self.request.user.pk
            new_event.title = self.request.POST.get('title')
            new_event.description = self.request.POST.get('description')
            new_event.charge_num = self.request.POST.get('charge_num')
            new_event.date = self.request.POST.get('date')
            new_event.start = start_date
            new_event.end = end_date
            if self.request.POST.get('to_do') == 'true':
                new_event.take_on_event = True
            new_event.save()
            group_obj.events.add(new_event)
            response = {
                "instance_id": new_event.id,
                "start_time": new_event.start,
                "end_time": new_event.end,
            }
            # send to client side.
            return JsonResponse(response, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)


def get_charge_users(request):
    event_obj = Event.objects.get(id=request.GET.get('event_id'))
    users_list = event_obj.get_charge_users()
    response_data = {'users_list': users_list}
    return JsonResponse(response_data)
