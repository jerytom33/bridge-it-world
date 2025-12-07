from django.urls import path
from .views import DashboardView, StudentRegistrationView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='student-dashboard'),
    path('register/', StudentRegistrationView.as_view(), name='student-register'),
]
