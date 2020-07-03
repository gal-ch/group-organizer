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
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    # permissions = forms.TypedMultipleChoiceField(
    #     choices=User._meta.permissions,
    #     coerce=get_permission_from_name,  )

    class Meta:
        model = Group
        fields = ('name', 'color')

    def __init__(self, *args, **kwargs):
        self.user = (kwargs.pop('user', None))
        print('user1', self.user)
        super().__init__(*args, **kwargs)
        self.fields['friends'].queryset = Friendship.objects.friends_of(self.user)
        print(Friendship.objects.friends_of(user=self.user))






