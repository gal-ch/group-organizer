from rest_framework import serializers
from accounts.models import FriendRequest, Friendship


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('sender',
                  'receiver',
                  'accepted',
                  )


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('user',
                  'friends',
                  )
