from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course-list'),
    path('<int:pk>/save/', views.SaveCourseView.as_view(), name='course-save'),
    path('<int:pk>/unsave/', views.UnsaveCourseView.as_view(), name='course-unsave'),
    path('saved/', views.SavedCoursesView.as_view(), name='saved-courses'),
]