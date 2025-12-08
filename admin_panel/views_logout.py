from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from courses.models import Course
from exams.models import Exam
from admin_panel.models import RoleUser as CustomUser
from admin_panel.decorators import admin_required

def home(request):
    """Home page view"""
    return render(request, 'home.html')

@admin_required
def admin_dashboard(request):
    # Get statistics
    total_users = CustomUser.objects.count()
    total_guides = CustomUser.objects.filter(role='guide').count()
    total_companies = CustomUser.objects.filter(role='company').count()
    total_courses = Course.objects.count()
    total_exams = Exam.objects.count()
    pending_approvals = CustomUser.objects.filter(is_approved=False).count()
    
    context = {
        'total_users': total_users,
        'total_guides': total_guides,
        'total_companies': total_companies,
        'total_courses': total_courses,
        'total_exams': total_exams,
        'pending_approvals': pending_approvals,
    }
    return render(request, 'admin_dashboard.html', context)

def admin_logout(request):
    """Admin logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
