from django.urls import path
from . import views

urlpatterns = [
    path('',             views.index,               name='index'),
    path('contact/',     views.contact,             name='contact'),
    path('track-time/',  views.track_time,          name='track_time'),
    path('track-event/', views.track_event,         name='track_event'),
    path('analytics/',   views.analytics_dashboard, name='analytics'),
]