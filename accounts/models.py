from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from events.models import Event
from django.contrib.auth import get_user_model
User = get_user_model()

COLORS = (
    ('blue', 'blue'),
    ('pink', 'pink'),
    ('red', 'red'),
    ('yellow', 'yellow'),
    ('green', 'green'),
)

Group.add_to_class('events', models.ManyToManyField(Event, related_name='events_group'))
Group.add_to_class('color', models.CharField(max_length=9,
                                             choices=COLORS,
                                             default="blue"))


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_to')
    # created = models.DateTimeField(default=datetime.datetime.now,editable=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} {self.receiver}'

    def accept(self):
        Friendship.objects.befriend(self.sender, self.receiver)
        self.accepted = True
        self.save()

    def decline(self):
        self.delete()


class FriendshipManager(models.Manager):
    def friends_of(self, user, shuffle=False):
        qs = User.objects.filter(friendship__friends__user=user)
        if shuffle:
            qs = qs.order_by('email')
        return qs

    def are_friends(self, user1, user2):
        return bool(Friendship.objects.get(user=user1).friends.filter(user=user2).exists())

    def befriend(self, user1, user2):
        Friendship.objects.get_or_create(user=user1).friends.add(
            Friendship.objects.get_or_create(user=user2))
        # delete any request by user1 to user2 so that we don't have ambiguous data
        FriendRequest.objects.filter(sender=user1, receiver=user2).delete()

    def unfriend(self, user1, user2):
        # Break friendship link between users
        Friendship.objects.get(user=user1).friends.remove(
            Friendship.objects.get(user=user2))
        # Delete FriendshipRequest's as well
        FriendRequest.objects.filter(sender=user1,
                                     receiver=user2).delete()
        FriendRequest.objects.filter(sender=user2,
                                     receiver=user1).delete()


class Friendship(models.Model):
    user = models.OneToOneField(User, related_name='friendship', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self')
    objects = FriendshipManager()

    def __str__(self):
        return self.user

    def friend_count(self):
        return self.friends.count()

