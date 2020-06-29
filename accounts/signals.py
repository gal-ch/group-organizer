from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import FriendRequest, Friendship


@receiver(post_save, sender=FriendRequest.accept())
def create_friendship_instance(sender, instance, created, **kwargs):
    if created:
        sender = instance.sender
        friend = instance.receiver
        friendship_sender_friend, created = Friendship.objects.get_or_create(user=sender)
        friendship_sender_friend.friends.add(friend)
        friendship_friend_sender, created = Friendship.objects.get_or_create(user=friend)
        friendship_friend_sender.friends.add(sender)
