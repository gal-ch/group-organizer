from django import template
register = template.Library()
from django.contrib.auth import get_user_model
User = get_user_model()


@register.filter
def get_name(id):
    name = User.objects.get(id=id).username
    return name
