from django.urls import path, include
from accounts import views
from accounts.views import JointLoginSignupView, GroupCreate

app_name = 'accounts'
urlpatterns = [
    path('accounts/login/', JointLoginSignupView.as_view(), name='login'),
    path('create-group/', GroupCreate.as_view(), name='create-group'),
    path('search-users-view/', views.search_users_view, name="search-users-view"),
    path('api/send-friend-request/', views.send_friend_request, name="send-friend-request"),
    path('api/response-to-friend-request/<int:pk>/', views.response_to_friend_request, name="response-to-friend-request"),

]
