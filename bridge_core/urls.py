from django.urls import path
from . import views

app_name = 'bridge_core'

urlpatterns = [
    path('career-path/', views.CareerPathListCreateView.as_view(), name='career-path-list-create'),
    path('career-path/<int:pk>/', views.CareerPathDetailView.as_view(), name='career-path-detail'),
    path('course/', views.CourseListCreateView.as_view(), name='course-list-create'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('mentor/', views.MentorListCreateView.as_view(), name='mentor-list-create'),
    path('mentor/<int:pk>/', views.MentorDetailView.as_view(), name='mentor-detail'),
    path('session/', views.MentorshipSessionListCreateView.as_view(), name='session-list-create'),
    path('session/<int:pk>/', views.MentorshipSessionDetailView.as_view(), name='session-detail'),
    path('resource/', views.ResourceListCreateView.as_view(), name='resource-list-create'),
    path('resource/<int:pk>/', views.ResourceDetailView.as_view(), name='resource-detail'),
]