from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
User = get_user_model()


class Event(models.Model):
    date = models.DateField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_events')
    take_on_event = models.BooleanField(default=False)
    charge_num = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    charge_users = models.ManyToManyField(User, related_name='in_charge_of', blank=True)

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        url = reverse('events:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    def get_charge_users(self):
        users_list = list(self.charge_users.all().values_list('username', flat=True))
        return users_list

    def check_if(self, user_id):
        ''' check if it possible to add the user to the in charge
        users list of the event and return response accordingly '''
        user = User.objects.get(id=user_id)
        if user in self.charge_users.all():
            # user already in this list
            return 0
        if self.charge_users.all().count() == self.charge_num:
            # list is full
            return 1
        self.charge_users.add(user)
        return 2















