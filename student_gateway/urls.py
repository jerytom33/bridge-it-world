from django.urls import path
from .views import DashboardView, StudentRegistrationView, StudentProfileView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='student-dashboard'),
    path('register/', StudentRegistrationView.as_view(), name='student-register'),
    path('profile/', StudentProfileView.as_view(), name='student-profile'),
]
