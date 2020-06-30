from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views
from accounts.views import JointLoginSignupView, GroupCreate

app_name = 'accounts'
urlpatterns = [
    path('accounts/login/', JointLoginSignupView.as_view(), name='login'),
    path('login-redirect/', views.login_redirect, name='login-redirect'),
    path('create-group/', GroupCreate.as_view(), name='create-group'),
    path("search-users-view/", views.search_users_view, name="search-users-view"),
    path("api/send-friend-request/", views.send_friend_request, name="send-friend-request"),
    path('api/response-to-friend-request/<int:pk>/', views.response_to_friend_request, name="response-to-friend-request"),

]
