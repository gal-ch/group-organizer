from django.contrib import admin
from accounts.models import FriendRequest, Friendship

admin.site.register(FriendRequest)
admin.site.register(Friendship)
