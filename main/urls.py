from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('get_users_list/', views.get_charge_users, name='ajax_get_users_list'),
]