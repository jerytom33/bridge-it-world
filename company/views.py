from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import CompanyProfile, JobPosting
from feed.models import Post
from django.contrib.auth.models import User
from admin_panel.models import RoleUser as UserProfile
from django.db.models import Sum

@login_required
def company_dashboard(request):
    # Check if user is a company
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile.role != 'company':
            messages.error(request, 'Access denied. Company access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if company is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your company account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get company profile
    try:
        company_profile = get_object_or_404(CompanyProfile, user=request.user)
    except Exception:
        company_profile = None
    
    # Get job postings
    job_postings = JobPosting.objects.filter(company__user=request.user).order_by('-created_at')
    
    # Get feed posts
    feed_posts = Post.objects.filter(author=request.user).order_by('-created_at')  # type: ignore
    
    # Get company exams and bootcamps
    company_exams = CompanyExam.objects.filter(company__user=request.user)
    company_bootcamps = CompanyBootcamp.objects.filter(company__user=request.user)
    
    # Calculate total views for all job postings
    total_views_result = job_postings.aggregate(total_views_sum=Sum('views_count'))
    total_views = total_views_result['total_views_sum'] or 0
    
    context = {
        'company_profile': company_profile,
        'job_postings': job_postings,
        'feed_posts': feed_posts,
        'company_exams': company_exams,
        'company_bootcamps': company_bootcamps,
        'total_views': total_views,
    }
    return render(request, 'company/dashboard.html', context)

@login_required
def update_company_profile(request):
    # Check if user is a company
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile.role != 'company':
            messages.error(request, 'Access denied. Company access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if company is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your company account is pending approval.')
        return redirect('admin_dashboard')
    
    try:
        company_profile = get_object_or_404(CompanyProfile, user=request.user)
    except Exception:
        company_profile = CompanyProfile(user=request.user)
    
    if request.method == 'POST':
        # Update company profile
        company_profile.company_name = request.POST.get('company_name', company_profile.company_name)
        company_profile.description = request.POST.get('description', company_profile.description)
        company_profile.website = request.POST.get('website', company_profile.website)
        company_profile.industry = request.POST.get('industry', company_profile.industry)
        company_profile.established = request.POST.get('established', company_profile.established)
        company_profile.employee_count = request.POST.get('employee_count', company_profile.employee_count)
        company_profile.location = request.POST.get('location', company_profile.location)
        company_profile.contact_email = request.POST.get('contact_email', company_profile.contact_email)
        company_profile.contact_phone = request.POST.get('contact_phone', company_profile.contact_phone)
        company_profile.save()
        messages.success(request, 'Company profile updated successfully!')
        return redirect('company_dashboard')
    
    context = {
        'company_profile': company_profile,
    }
    return render(request, 'company/update_profile.html', context)

@login_required
def create_job_posting(request):
    # Check if user is a company
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile.role != 'company':
            messages.error(request, 'Access denied. Company access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if company is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your company account is pending approval.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        try:
            company_profile = get_object_or_404(CompanyProfile, user=request.user)
        except Exception:
            messages.error(request, 'Please complete your company profile first.')
            return redirect('update_company_profile')
        
        # Create job posting
        job_posting = JobPosting(
            company=company_profile,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            job_type=request.POST.get('job_type'),
            experience_level=request.POST.get('experience_level'),
            location=request.POST.get('location'),
            salary_range=request.POST.get('salary_range', ''),
            application_deadline=request.POST.get('application_deadline'),
        )
        job_posting.save()
        
        # Create a feed post for this job
        feed_post = Post(
            author=request.user,
            content=f"New job opening: {job_posting.title}\n\n{job_posting.description}",
            post_type='text',
        )
        feed_post.save()
        
        messages.success(request, 'Job posting created successfully!')
        return redirect('company_dashboard')
    
    return render(request, 'company/create_job.html')

@login_required
def view_job_postings(request):
    # Check if user is a company
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile.role != 'company':
            messages.error(request, 'Access denied. Company access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if company is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your company account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get job postings
    job_postings = JobPosting.objects.filter(company__user=request.user).order_by('-created_at')
    
    context = {
        'job_postings': job_postings,
    }
    return render(request, 'company/view_jobs.html', context)

@login_required
def view_feed_posts(request):
    # Check if user is a company
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile.role != 'company':
            messages.error(request, 'Access denied. Company access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if company is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your company account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get feed posts
    feed_posts = Post.objects.filter(author=request.user).order_by('-created_at')  # type: ignore
    
    context = {
        'feed_posts': feed_posts,
    }
    return render(request, 'company/view_posts.html', context)

def company_login(request):
    """View for company login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is a company
            try:
                user_profile = get_object_or_404(UserProfile, user=user)
                if user_profile.role == 'company':
                    # Check if company is approved
                    if not user_profile.is_approved:
                        messages.error(request, 'Your company account is pending approval.')
                        return redirect('company_login')
                    login(request, user)
                    return redirect('company_dashboard')
                else:
                    messages.error(request, 'Access denied. This account is not a company account.')
            except Exception:
                messages.error(request, 'User profile not found.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'company/login.html')


@login_required
def create_feed_post(request):
    """View for creating a new feed post"""
    # Check if user is a company
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile.role != 'company':
            messages.error(request, 'Access denied. Company access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if company is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your company account is pending approval.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        post_type = request.POST.get('post_type', 'text')
        media_url = request.POST.get('media_url', '')
        
        if not content:
            messages.error(request, 'Content is required.')
            return redirect('view_feed_posts')
        
        # Create feed post
        feed_post = Post(
            author=request.user,
            content=content,
            post_type=post_type,
            media_url=media_url if media_url else '',
        )
        feed_post.save()
        
        messages.success(request, 'Post created successfully!')
        return redirect('view_feed_posts')
    
    return redirect('view_feed_posts')


@login_required
def company_analytics(request):
    """View for displaying company engagement analytics"""
    # Check if user is a company
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile.role != 'company':
            messages.error(request, 'Access denied. Company access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if company is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your company account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get company's feed posts with engagement metrics
    company_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    # Calculate totals
    total_views = sum(post.views_count for post in company_posts)
    total_likes = sum(post.likes_count for post in company_posts)
    total_comments = sum(post.comments_count for post in company_posts)
    
    # Get top performing posts
    top_posts = company_posts.order_by('-views_count')[:5]
    
    context = {
        'company_posts': company_posts,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'top_posts': top_posts,
    }
    return render(request, 'company/analytics.html', context)


@login_required
def create_company_exam(request):
    """View for creating a company-specific exam"""
    # Check if user is a company
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile.role != 'company':
            messages.error(request, 'Access denied. Company access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if company is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your company account is pending approval.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        try:
            company_profile = get_object_or_404(CompanyProfile, user=request.user)
        except Exception:
            messages.error(request, 'Please complete your company profile first.')
            return redirect('update_company_profile')
        
        # Create company exam
        company_exam = CompanyExam(
            company=company_profile,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            exam_date=request.POST.get('exam_date'),
            registration_deadline=request.POST.get('registration_deadline'),
            level=request.POST.get('level'),
            link=request.POST.get('link', ''),
        )
        company_exam.save()
        
        messages.success(request, 'Company exam created successfully!')
        return redirect('view_company_exams')
    
    return render(request, 'company/create_exam.html')


@login_required
def view_company_exams(request):
    """View for displaying company's exams"""
    # Check if user is a company
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile.role != 'company':
            messages.error(request, 'Access denied. Company access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if company is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your company account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get company exams
    company_exams = CompanyExam.objects.filter(company__user=request.user).order_by('-created_at')
    
    context = {
        'company_exams': company_exams,
    }
    return render(request, 'company/view_exams.html', context)


@login_required
def create_company_bootcamp(request):
    """View for creating a company-specific bootcamp"""
    # Check if user is a company
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile.role != 'company':
            messages.error(request, 'Access denied. Company access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if company is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your company account is pending approval.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        try:
            company_profile = get_object_or_404(CompanyProfile, user=request.user)
        except Exception:
            messages.error(request, 'Please complete your company profile first.')
            return redirect('update_company_profile')
        
        # Create company bootcamp
        company_bootcamp = CompanyBootcamp(
            company=company_profile,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            duration=request.POST.get('duration'),
            price=request.POST.get('price', None),
            link=request.POST.get('link', ''),
            is_certified=request.POST.get('is_certified', False),
        )
        company_bootcamp.save()
        
        messages.success(request, 'Company bootcamp created successfully!')
        return redirect('view_company_bootcamps')
    
    return render(request, 'company/create_bootcamp.html')


@login_required
def view_company_bootcamps(request):
    """View for displaying company's bootcamps"""
    # Check if user is a company
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile.role != 'company':
            messages.error(request, 'Access denied. Company access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if company is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your company account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get company bootcamps
    company_bootcamps = CompanyBootcamp.objects.filter(company__user=request.user).order_by('-created_at')
    
    context = {
        'company_bootcamps': company_bootcamps,
    }
    return render(request, 'company/view_bootcamps.html', context)


def company_logout(request):
    """View for company logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('company_login')
