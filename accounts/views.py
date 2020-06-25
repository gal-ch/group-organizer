from allauth.account.views import *
from allauth.account.app_settings import *
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from accounts.forms import EditGroupForm
User = get_user_model()


class JointLoginSignupView(LoginView):
    form_class = LoginForm
    signup_form = SignupForm
    template_name = 'account/login.html'

    def __init__(self, **kwargs):
        super(JointLoginSignupView, self).__init__(*kwargs)

    def get_context_data(self, **kwargs):
        ret = super(JointLoginSignupView, self).get_context_data(**kwargs)
        ret['signup_form'] = get_form_class(app_settings.FORMS, 'signup', self.signup_form)
        return ret


login = JointLoginSignupView.as_view()


class GroupCreate(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': EditGroupForm()}
        return render(request, 'account/group_create.html', context)

    def post(self, request, *args, **kwargs):
        form = EditGroupForm(request.POST)
        '''create a group -> add users -> give the created user perm to change the group '''
        user = User.objects.get(id=request.user.pk)
        perm = Permission.objects.get(codename='change_group')
        user.user_permissions.add(perm)
        user.save()
        print(user.user_permissions)
        print(user.has_perm('auth.change_group'))
        if form.is_valid():
            group_name = request.POST.get('group_name')
            new_group = Group.objects.create(name=group_name)
            users = [User.objects.get(pk=pk) for pk in request.POST.getlist("users", "")]
            for user in users:
                new_group.user_set.add(user)
            return HttpResponseRedirect('main:calendar', kwargs={'pk': new_group.id})
        return render(request, 'account/group_create.html', {'form': form})

