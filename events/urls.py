from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('event-create/', views.EventCreate.as_view(), name='event-create'),
    path('event-update/', views.update_event, name='event-update'),
    path('ajax_event_change_date/', views.event_change_date, name='ajax_event_change_date'),




]