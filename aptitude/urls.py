from django.urls import path
from . import views

app_name = 'aptitude'

urlpatterns = [
    path('questions/', views.AptitudeQuestionsView.as_view(), name='aptitude-questions'),
    path('submit/', views.SubmitAptitudeTestView.as_view(), name='aptitude-submit'),
    path('history/', views.AptitudeHistoryView.as_view(), name='aptitude-history'),
    
    # MegaLLM AI-powered endpoints
    path('personalized-questions/', views.PersonalizedAptitudeQuestionsView.as_view(), name='personalized-questions'),
    path('analyze-results/', views.AnalyzeAptitudeResultsView.as_view(), name='analyze-results'),
    
    # Browser test page
    path('test/', views.aptitude_test_page, name='aptitude-test-page'),
]