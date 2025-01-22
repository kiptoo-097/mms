from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registration
    path('signup/', views.SignUpView.as_view(), name='signup'),
    
    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    
    # Password
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
]