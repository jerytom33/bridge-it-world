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

@admin_required
def manage_guides_companies(request):
    # Get pending approvals
    pending_guides = CustomUser.objects.filter(role='guide', is_approved=False)
    pending_companies = CustomUser.objects.filter(role='company', is_approved=False)
    
    # Get approved guides and companies
    approved_guides = CustomUser.objects.filter(role='guide', is_approved=True)
    approved_companies = CustomUser.objects.filter(role='company', is_approved=True)
    
    context = {
        'pending_guides': pending_guides,
        'pending_companies': pending_companies,
        'approved_guides': approved_guides,
        'approved_companies': approved_companies,
    }
    return render(request, 'manage_guides_companies.html', context)

@admin_required
def approve_guide(request, guide_id):
    """Approve a guide application"""
    if request.method == 'POST':
        try:
            guide = CustomUser.objects.get(id=guide_id, role='guide')
            guide.is_approved = True
            guide.save()
            messages.success(request, f'Guide {guide.user.username} has been approved successfully.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Guide not found.')
        except Exception as e:
            messages.error(request, f'Error approving guide: {str(e)}')
    return redirect('manage_guides_companies')

@admin_required
def reject_guide(request, guide_id):
    """Reject a guide application"""
    if request.method == 'POST':
        try:
            guide = CustomUser.objects.get(id=guide_id, role='guide')
            # Delete the user account
            user = guide.user
            guide.delete()
            user.delete()
            messages.success(request, 'Guide application has been rejected and removed.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Guide not found.')
        except Exception as e:
            messages.error(request, f'Error rejecting guide: {str(e)}')
    return redirect('manage_guides_companies')

@admin_required
def approve_company(request, company_id):
    """Approve a company application"""
    if request.method == 'POST':
        try:
            company = CustomUser.objects.get(id=company_id, role='company')
            company.is_approved = True
            company.save()
            messages.success(request, f'Company {company.user.username} has been approved successfully.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Company not found.')
        except Exception as e:
            messages.error(request, f'Error approving company: {str(e)}')
    return redirect('manage_guides_companies')

@admin_required
def reject_company(request, company_id):
    """Reject a company application"""
    if request.method == 'POST':
        try:
            company = CustomUser.objects.get(id=company_id, role='company')
            # Delete the user account
            user = company.user
            company.delete()
            user.delete()
            messages.success(request, 'Company application has been rejected and removed.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Company not found.')
        except Exception as e:
            messages.error(request, f'Error rejecting company: {str(e)}')
    return redirect('manage_guides_companies')

def admin_logout(request):
    """Admin logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@admin_required
def manage_exams(request):
    """View and manage exams (view/delete only)"""
    # Get all exams
    exams = Exam.objects.all()
    
    context = {
        'exams': exams,
    }
    return render(request, 'manage_exams.html', context)

@admin_required
def delete_exam(request, exam_id):
    """Delete an exam"""
    if request.method == 'POST':
        try:
            exam = Exam.objects.get(id=exam_id)
            exam_title = exam.title
            exam.delete()
            messages.success(request, f'Exam "{exam_title}" has been deleted successfully!')
        except Exam.DoesNotExist:
            messages.error(request, 'Exam not found.')
        except Exception as e:
            messages.error(request, f'Error deleting exam: {str(e)}')
    
    return redirect('admin_manage_exams')

@admin_required
def manage_courses(request):
    """View and manage courses (view/delete only)"""
    # Get all courses
    courses = Course.objects.all()
    
    context = {
        'courses': courses,
    }
    return render(request, 'manage_courses.html', context)

@admin_required
def delete_course(request, course_id):
    """Delete a course"""
    if request.method == 'POST':
        try:
            course = Course.objects.get(id=course_id)
            course_title = course.title
            course.delete()
            messages.success(request, f'Course "{course_title}" has been deleted successfully!')
        except Course.DoesNotExist:
            messages.error(request, 'Course not found.')
        except Exception as e:
            messages.error(request, f'Error deleting course: {str(e)}')
    
    return redirect('admin_manage_courses')

@admin_required
def manage_users(request):
    # Get all users
    all_users = CustomUser.objects.all()
    blocked_users = CustomUser.objects.filter(is_blocked=True)
    
    context = {
        'all_users': all_users,
        'blocked_users': blocked_users,
    }
    return render(request, 'manage_users.html', context)

@admin_required
def admin_stats(request):
    # Get statistics for the stats page
    total_users = CustomUser.objects.count()
    total_guides = CustomUser.objects.filter(role='guide').count()
    total_companies = CustomUser.objects.filter(role='company').count()
    total_courses = Course.objects.count()
    total_exams = Exam.objects.count()
    
    # Get user distribution by role
    students_count = CustomUser.objects.filter(role='student').count()
    guides_count = CustomUser.objects.filter(role='guide').count()
    companies_count = CustomUser.objects.filter(role='company').count()
    admins_count = CustomUser.objects.filter(role='admin').count()
    
    context = {
        'total_users': total_users,
        'total_guides': total_guides,
        'total_companies': total_companies,
        'total_courses': total_courses,
        'total_exams': total_exams,
        'students_count': students_count,
        'guides_count': guides_count,
        'companies_count': companies_count,
        'admins_count': admins_count,
    }
    return render(request, 'admin_stats.html', context)

def register_guide(request):
    """View for guide registration form"""
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        expertise = request.POST.get('expertise')
        experience_years = request.POST.get('experience_years')
        company = request.POST.get('company')
        position = request.POST.get('position')
        linkedin_url = request.POST.get('linkedin_url')
        
        # Basic validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register_guide.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register_guide.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'register_guide.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create guide role profile in RoleUser
        guide_role = CustomUser.objects.create(
            user=user,
            role='guide',
            is_approved=False,  # Pending approval
            phone=phone
        )
        
        # Also create a GuideProfile for additional details
        try:
            from guide.models import GuideProfile
            GuideProfile.objects.create(
                user=user,
                bio=bio,
                expertise=[e.strip() for e in expertise.split(',')] if expertise else [],
                experience_years=experience_years,
                company=company,
                position=position,
                linkedin_url=linkedin_url
            )
        except ImportError:
            # If GuideProfile model doesn't exist, continue without it
            pass
        
        messages.success(request, 'Your application has been submitted successfully. Our team will review it within 3-5 business days.')
        return redirect('register_guide')
    
    return render(request, 'register_guide.html')

def register_company(request):
    """View for company registration form"""
    if request.method == 'POST':
        # Get form data
        company_name = request.POST.get('company_name')
        contact_person = request.POST.get('contact_person')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        website = request.POST.get('website')
        industry = request.POST.get('industry')
        established = request.POST.get('established')
        employee_count = request.POST.get('employee_count')
        location = request.POST.get('location')
        description = request.POST.get('description')
        job_roles = request.POST.get('job_roles')
        
        # Basic validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register_company.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register_company.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'register_company.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=company_name,
            last_name=contact_person
        )
        
        # Create company profile in CustomUser
        company_profile = CustomUser.objects.create(
            user=user,
            role='company',
            is_approved=False,  # Pending approval
            phone=phone
        )
        
        # Also create a CompanyProfile for additional details
        try:
            from company.models import CompanyProfile
            
            # Handle empty numeric fields
            established_year = int(established) if established and established.strip() else None
            employee_count_int = int(employee_count) if employee_count and employee_count.strip() else None
            
            CompanyProfile.objects.create(
                user=user,
                company_name=company_name,
                description=description,
                website=website,
                industry=industry,
                established=established_year,
                employee_count=employee_count_int,
                location=location,
                contact_email=email,
                contact_phone=phone
            )
        except ImportError:
            # If CompanyProfile model doesn't exist, continue without it
            pass
        except ValueError as e:
            # If there's a value error with numeric fields, log it but continue
            messages.warning(request, 'Some optional fields were not saved due to invalid format.')
        
        messages.success(request, 'Your company registration has been submitted successfully. Our team will review it within 3-5 business days.')
        return redirect('register_company')
    
    return render(request, 'register_company.html')
