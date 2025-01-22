from django.urls import path
from . import views

app_name = 'radio'

urlpatterns = [
    path('', views.RadioPlayerView.as_view(), name='player'),
    path('schedule/', views.ScheduleView.as_view(), name='schedule'),
]