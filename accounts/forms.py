from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from accounts.models import Friendship

User = get_user_model()


def get_permission_from_name(name):
    return Permission.objects.get(name=name)


class EditGroupForm(forms.ModelForm):
    friends = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple())

    # permissions = forms.TypedMultipleChoiceField(
    #     choices=User._meta.permissions,
    #     coerce=get_permission_from_name,  )

    class Meta:
        model = Group
        fields = ('name', 'color')

    def __init__(self,user, *args, **kwargs):
        print('user1', user)
        super().__init__(*args, **kwargs)
        self.fields['friends'].queryset = Friendship.objects.friends_of(user=user)
        print(Friendship.objects.friends_of(user=user))






