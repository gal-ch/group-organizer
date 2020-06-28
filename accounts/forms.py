from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
User = get_user_model()


def get_permission_from_name(name):
    return Permission.objects.get(name=name)


class EditGroupForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple())
    # permissions = forms.TypedMultipleChoiceField(
    #     choices=User._meta.permissions,
    #     coerce=get_permission_from_name,  )

    class Meta:
        model = Group
        fields = ('name', 'color')




