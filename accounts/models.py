from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event
COLORS = (
    ('BLUE', 'blue'),
    ('PINK', 'pink'),
    ('RED', 'red'),
    ('YELLOW', 'yellow'),
    ('GREEN', 'green'),
)

Group.add_to_class('events', models.ManyToManyField(Event, related_name='events_group'))
Group.add_to_class('color', models.CharField(max_length=9,
                                             choices=COLORS,
                                             default="BLUE"))
