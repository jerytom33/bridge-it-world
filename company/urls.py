from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.company_dashboard, name='company_dashboard'),
    path('profile/update/', views.update_company_profile, name='update_company_profile'),
    path('jobs/create/', views.create_job_posting, name='create_job_posting'),
    path('jobs/', views.view_job_postings, name='view_job_postings'),
    path('posts/', views.view_feed_posts, name='view_feed_posts'),
    path('posts/create/', views.create_feed_post, name='create_feed_post'),
    path('analytics/', views.company_analytics, name='company_analytics'),
    path('exams/create/', views.create_company_exam, name='create_company_exam'),
    path('exams/', views.view_company_exams, name='view_company_exams'),
    path('bootcamps/create/', views.create_company_bootcamp, name='create_company_bootcamp'),
    path('bootcamps/', views.view_company_bootcamps, name='view_company_bootcamps'),
    path('login/', views.company_login, name='company_login'),
    path('logout/', views.company_logout, name='company_logout'),
]