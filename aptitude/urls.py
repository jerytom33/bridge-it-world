from django.urls import path
from . import views

app_name = 'aptitude'

urlpatterns = [
    path('questions/', views.AptitudeQuestionsView.as_view(), name='aptitude-questions'),
    path('submit/', views.SubmitAptitudeTestView.as_view(), name='aptitude-submit'),
    path('history/', views.AptitudeHistoryView.as_view(), name='aptitude-history'),
]