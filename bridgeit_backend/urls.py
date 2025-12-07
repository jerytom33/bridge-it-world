from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from admin_panel import views as admin_views
from django.conf import settings
from django.conf.urls.static import static

def home_view(request):
    return JsonResponse({
        "message": "Welcome to BridgeIT Backend API",
        "version": "1.0",
        "endpoints": {
            "admin": "/admin/",
            "core_api": "/api/core/",
            "bridge_api": "/api/bridge/",
            "auth": "/api/auth/",
            "admin_panel": "/admin-panel/",
            "company": "/company/",
            "guide": "/guide/",
            "resume": "/api/resume/",
            "aptitude": "/api/aptitude/",
            "exams": "/api/exams/",
            "courses": "/api/courses/",
            "feed": "/api/feed/",
            "student_gateway": "/api/student/"
        }
    })

urlpatterns = [
    path('', admin_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('api/core/', include('core.urls')),
    path('api/bridge/', include('bridge_core.urls')),
    path('api/auth/', include('users.urls')),  # Updated: User auth endpoints
    path('api/student/', include('student_gateway.urls')), # Student Gateway
    path('admin-panel/', include('admin_panel.urls')),
    path('company/', include('company.urls')),
    path('guide/', include('guide.urls')),
    # Student app endpoints
    path('api/resume/', include('resume.urls')),
    path('api/aptitude/', include('aptitude.urls')),
    path('api/exams/', include('exams.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/feed/', include('feed.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
]