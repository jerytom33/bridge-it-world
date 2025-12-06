from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('guides-companies/', views.manage_guides_companies, name='manage_guides_companies'),
    path('exams/', views.manage_exams, name='admin_manage_exams'),
    path('exams/delete/<int:exam_id>/', views.delete_exam, name='admin_delete_exam'),
    path('courses/', views.manage_courses, name='admin_manage_courses'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='admin_delete_course'),
    path('users/', views.manage_users, name='manage_users'),
    path('stats/', views.admin_stats, name='admin_stats'),
    path('register-guide/', views.register_guide, name='register_guide'),
    path('register-company/', views.register_company, name='register_company'),
    path('approve-guide/<int:guide_id>/', views.approve_guide, name='approve_guide'),
    path('reject-guide/<int:guide_id>/', views.reject_guide, name='reject_guide'),
    path('approve-company/<int:company_id>/', views.approve_company, name='approve_company'),
    path('reject-company/<int:company_id>/', views.reject_company, name='reject_company'),
    path('logout/', views.admin_logout, name='admin_logout'),
]