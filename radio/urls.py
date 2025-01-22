from django.urls import path
from . import views

app_name = 'radio'

urlpatterns = [
    path('', views.player, name='player'),
    path('schedule/', views.schedule, name='schedule'),
]