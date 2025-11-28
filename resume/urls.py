from django.urls import path
from . import views

app_name = 'resume'

urlpatterns = [
    path('upload/', views.ResumeUploadView.as_view(), name='resume-upload'),
    path('history/', views.ResumeHistoryView.as_view(), name='resume-history'),
]