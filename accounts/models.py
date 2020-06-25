from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event
Group.add_to_class('events', models.ManyToManyField(Event,  related_name='events_group'))


