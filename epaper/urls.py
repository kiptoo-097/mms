from django.urls import path
from . import views

app_name = 'epaper'

urlpatterns = [
    path('', views.epaper_list, name='list'),
    path('<slug:slug>/', views.epaper_detail, name='detail'),
    path('download/<slug:slug>/', views.epaper_download, name='download'),
]