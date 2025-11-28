from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.ExamListView.as_view(), name='exam-list'),
    path('<int:pk>/save/', views.SaveExamView.as_view(), name='exam-save'),
    path('<int:pk>/unsave/', views.UnsaveExamView.as_view(), name='exam-unsave'),
    path('saved/', views.SavedExamsView.as_view(), name='saved-exams'),
]