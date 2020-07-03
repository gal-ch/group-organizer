from allauth.account.views import *
from allauth.account.app_settings import *
from django.contrib.auth.models import Group, Permission
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from accounts.forms import EditGroupForm
from accounts.models import FriendRequest, Friendship
from accounts.serializers import FriendshipSerializer, FriendRequestSerializer
from rest_framework import status
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
    form_class = EditGroupForm
    template_name = 'account/group_create.html'

    def get_form_kwargs(self):
        kwargs = super(GroupCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        form = EditGroupForm(request.POST, user=request.user)
        '''create a group -> add users -> give the created user perm to change the group '''
        current_user = User.objects.get(id=request.user.pk)
        perm = Permission.objects.get(codename='change_group')
        current_user.user_permissions.add(perm)
        current_user.save()
        print(current_user.user_permissions)
        print(current_user.has_perm('auth.change_group'))
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.save()
            new_group.user_set.add(current_user)
            friends = [User.objects.get(pk=pk) for pk in request.POST.getlist("friends", "")]
            print(friends)
            for friend in friends:
                new_group.user_set.add(friend)
            print('new_group.user_set.all()',new_group.user_set.all())
            return redirect('main:calendar')
        return render(request, 'account/group_create.html', {'form': form})


def search_users_view(request):
    url_parameter = request.GET.get("q")
    user_friends = None
    if url_parameter:
        user_friends = Friendship.objects.friends_of(user=request.user)
        user_friends_id_list = Friendship.objects.friends_of(user=request.user).values('id')
        user_not_friends = User.objects.filter(email__icontains=url_parameter).exclude(id__in=user_friends_id_list).exclude(id=request.user.pk)
    else:
        user_not_friends = User.objects.all()
    if request.is_ajax():
        html = render_to_string(
            template_name="account/users_search_result.html",
            context={
                "user_not_friends": user_not_friends,
                "friends_users": user_friends,
            }
        )
        print(user_not_friends)
        print(user_friends)
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)


# to do ---> fix serializer
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def send_friend_request(request):
    data = request.data
    sender = request.user
    receiver = User.objects.get(id=data['receiver_id'])
    friends_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
    if created:
        # friends_request_serializer = FriendRequestSerializer(data={'sender':sender, 'receiver':receiver})
        # if friends_request_serializer.is_valid():
        #     friends_request_serializer.save()
            return JsonResponse({'success': 'success friend request send'}, status=200)
    elif not created and friends_request:
        return JsonResponse({'exists': 'you and {} already friends'.format(receiver.username)}, status=200)
    return JsonResponse({"error": ''}, status=400)


# to fix
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def response_to_friend_request(request, pk):
    user2 = User.objects.get(id=pk)
    response = request.data['response']
    if response is True:
        # create friendship between the two and delete the friendship request
        friendship1, create = Friendship.objects.get_or_create(user=user2)
        friendship2, create = Friendship.objects.get_or_create(user=request.user)
        friendship2.friends.add(friendship1)
        friendship_request = FriendRequest.objects.get(sender=user2, receiver=request.user).delete()
        # friendship_serializer = FriendshipSerializer(data=friendship)
        # print(friendship)
        # if friendship_serializer.is_valid():
        #     friendship_serializer.save()
        return JsonResponse({'success': 'friend request approve'}, status=status.HTTP_201_CREATED)
    else:
        FriendRequest.objects.get(sender=user2, receiver=request.user).decline()
        return JsonResponse({'success': 'friend request decline'}, status=200)
  #  return JsonResponse({"error": ''}, status=status.HTTP_400_BAD_REQUEST)



