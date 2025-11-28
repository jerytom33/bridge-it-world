from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.guide_dashboard, name='guide_dashboard'),
    path('profile/update/', views.update_guide_profile, name='update_guide_profile'),
    path('exams/', views.manage_exams, name='manage_exams'),
    path('exams/add/', views.add_exam, name='add_exam'),
    path('exams/edit/<int:exam_id>/', views.edit_exam, name='edit_exam'),
    path('exams/delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('courses/', views.manage_courses, name='manage_courses'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('posts/create/', views.create_post, name='create_post'),
    path('login/', views.guide_login, name='guide_login'),
]