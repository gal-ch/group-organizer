from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('ajax_event_change_date/', views.event_change_date, name='ajax_event_change_date'),
    path('api/event-update-users/<int:pk>/', views.event_update_users, name="event-update-users"),
    path('api/update-event-source/<int:pk>/', views.update_event_source, name="update-event-source"),

]
