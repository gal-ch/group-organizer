from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('event-create/', views.EventCreate.as_view(), name='event-create'),
    path('ajax_event_change_date/', views.event_change_date, name='ajax_event_change_date'),
    path('event-detail/<int:pk>/', views.eventDetail, name="event-detail"),
    path('event-update-users/<int:pk>/', views.eventUpdate, name="event-update-users"),



]