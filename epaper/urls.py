from django.urls import path
from . import views

app_name = 'epaper'

urlpatterns = [
    path('', views.EpaperListView.as_view(), name='list'),
    path('<slug:slug>/', views.EpaperDetailView.as_view(), name='detail'),
    path('download/<slug:slug>/', views.epaper_download, name='download'),
]