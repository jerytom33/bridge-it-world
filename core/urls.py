from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('profile/', views.ProfileListCreateView.as_view(), name='profile-list-create'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('exam/', views.ExamListCreateView.as_view(), name='exam-list-create'),
    path('exam/<int:pk>/', views.ExamDetailView.as_view(), name='exam-detail'),
    path('user/', views.current_user, name='current-user'),
    path('login/', views.LoginAPI.as_view(), name='login_api'),
    path('profile-api/', views.ProfileAPI.as_view(), name='profile_api'),
    path('resume/upload/', views.ResumeUploadAPI.as_view(), name='resume_upload_api'),
    # FIXED: Added signup path
    path('user_signup/', views.signup_view, name='user_signup'),
    # Student profile endpoints
    path('profile/setup/', views.ProfileAPI.as_view(), name='profile-setup'),
    path('profile/me/', views.ProfileAPI.as_view(), name='profile-me'),
    # Notification endpoints
    path('notifications/', views.NotificationListView.as_view(), name='notifications-list'),
    path('notifications/<int:notification_id>/mark-read/', views.MarkNotificationReadView.as_view(), name='notification-mark-read'),
    path('notifications/mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='notifications-mark-all-read'),
    # FCM Endpoints
    path('fcm/register/', views.FCMTokenView.as_view(), name='fcm-register'),
    path('fcm/test/', views.TestNotificationView.as_view(), name='fcm-test'),
]
