# urls.py
from django.urls import path
from .views import SignupView, LoginView, ProfileSetupView, ProfileView

urlpatterns = [
    path('register/', SignupView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/setup/', ProfileSetupView.as_view(), name='profile-setup'),
    path('me/', ProfileView.as_view(), name='profile'),
]