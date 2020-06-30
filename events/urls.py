from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('event-create/', views.EventCreate.as_view(), name='event-create'),
    path('ajax_event_change_date/', views.event_change_date, name='ajax_event_change_date'),
    path('api/event-detail/<int:pk>/', views.event_detail, name="event-detail"),
    path('api/event-update-users/<int:pk>/', views.event_update_users, name="event-update-users"),
    path('api/update-event-source/<int:pk>/', views.update_event_source, name="update-event-source"),



]