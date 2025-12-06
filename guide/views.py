from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from .models import GuideProfile, GuideExam, GuideCourse
from admin_panel.models import RoleUser  # Changed from RoleUser to RoleUser
from exams.models import Exam
from courses.models import Course
from feed.models import Post

@login_required
def guide_dashboard(request):
    # Check if user is a guide
    try:
        user_profile = get_object_or_404(RoleUser, user=request.user)
        if user_profile.role != 'guide':
            messages.error(request, 'Access denied. Guide access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if guide is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your guide account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get guide profile
    try:
        guide_profile = get_object_or_404(GuideProfile, user=request.user)
    except Exception:
        guide_profile = None
    
    # Get stats
    total_exams = Exam.objects.count()  # type: ignore
    total_courses = Course.objects.count()  # type: ignore
    total_posts = Post.objects.filter(author=request.user).count()  # type: ignore
    
    context = {
        'guide_profile': guide_profile,
        'total_exams': total_exams,
        'total_courses': total_courses,
        'total_posts': total_posts,
    }
    return render(request, 'guide/dashboard.html', context)

@login_required
def update_guide_profile(request):
    # Check if user is a guide
    try:
        user_profile = get_object_or_404(RoleUser, user=request.user)
        if user_profile.role != 'guide':
            messages.error(request, 'Access denied. Guide access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if guide is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your guide account is pending approval.')
        return redirect('admin_dashboard')
    
    try:
        guide_profile = get_object_or_404(GuideProfile, user=request.user)
    except Exception:
        guide_profile = GuideProfile(user=request.user)
    
    if request.method == 'POST':
        # Update guide profile
        guide_profile.bio = request.POST.get('bio', guide_profile.bio)
        expertise_input = request.POST.get('expertise', '')
        guide_profile.expertise = [e.strip() for e in expertise_input.split(',') if e.strip()] if expertise_input else []
        guide_profile.experience_years = request.POST.get('experience_years', guide_profile.experience_years)
        guide_profile.company = request.POST.get('company', guide_profile.company)
        guide_profile.position = request.POST.get('position', guide_profile.position)
        guide_profile.linkedin_url = request.POST.get('linkedin_url', guide_profile.linkedin_url)
        guide_profile.save()
        messages.success(request, 'Guide profile updated successfully!')
        return redirect('guide_dashboard')
    
    context = {
        'guide_profile': guide_profile,
    }
    return render(request, 'guide/update_profile.html', context)

@login_required
def manage_exams(request):
    # Check if user is a guide
    try:
        user_profile = get_object_or_404(RoleUser, user=request.user)
        if user_profile.role != 'guide':
            messages.error(request, 'Access denied. Guide access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if guide is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your guide account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get all exams
    exams = Exam.objects.all().order_by('-created_at')  # type: ignore
    
    context = {
        'exams': exams,
    }
    return render(request, 'guide/manage_exams.html', context)

@login_required
def add_exam(request):
    # Check if user is a guide
    try:
        user_profile = get_object_or_404(RoleUser, user=request.user)
        if user_profile.role != 'guide':
            messages.error(request, 'Access denied. Guide access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if guide is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your guide account is pending approval.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        # Create a new exam
        exam = Exam(
            title=request.POST.get('title', ''),
            category=request.POST.get('category', ''),
            level=request.POST.get('level', '10th'),
            last_date=request.POST.get('last_date', ''),
            link=request.POST.get('link', ''),
            description=request.POST.get('description', ''),
        )
        exam.save()  # type: ignore
        
        # Link exam to guide
        guide_exam = GuideExam(
            guide=request.user,
            exam=exam
        )
        guide_exam.save()
        
        messages.success(request, 'Exam added successfully!')
        return redirect('manage_exams')
    
    return render(request, 'guide/add_exam.html')

@login_required
def edit_exam(request, exam_id):
    # Check if user is a guide
    try:
        user_profile = get_object_or_404(RoleUser, user=request.user)
        if user_profile.role != 'guide':
            messages.error(request, 'Access denied. Guide access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if guide is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your guide account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get the exam
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        # Update the exam
        exam.title = request.POST.get('title', exam.title)
        exam.category = request.POST.get('category', exam.category)
        exam.level = request.POST.get('level', exam.level)
        exam.last_date = request.POST.get('last_date', exam.last_date)
        exam.link = request.POST.get('link', exam.link)
        exam.description = request.POST.get('description', exam.description)
        exam.save()
        
        messages.success(request, 'Exam updated successfully!')
        return redirect('manage_exams')
    
    context = {
        'exam': exam,
    }
    return render(request, 'guide/edit_exam.html', context)

@login_required
def delete_exam(request, exam_id):
    # Check if user is a guide
    try:
        user_profile = get_object_or_404(RoleUser, user=request.user)
        if user_profile.role != 'guide':
            messages.error(request, 'Access denied. Guide access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if guide is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your guide account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get the exam
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        # Delete the exam
        exam.delete()
        messages.success(request, 'Exam deleted successfully!')
        return redirect('manage_exams')
    
    context = {
        'exam': exam,
    }
    return render(request, 'guide/delete_exam.html', context)

@login_required
def manage_courses(request):
    # Check if user is a guide
    try:
        user_profile = get_object_or_404(RoleUser, user=request.user)
        if user_profile.role != 'guide':
            messages.error(request, 'Access denied. Guide access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if guide is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your guide account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get all courses
    courses = Course.objects.all().order_by('-created_at')  # type: ignore
    
    context = {
        'courses': courses,
    }
    return render(request, 'guide/manage_courses.html', context)

@login_required
def add_course(request):
    # Check if user is a guide
    try:
        user_profile = get_object_or_404(RoleUser, user=request.user)
        if user_profile.role != 'guide':
            messages.error(request, 'Access denied. Guide access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if guide is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your guide account is pending approval.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        # Create a new course
        course = Course(
            title=request.POST.get('title', ''),
            provider=request.POST.get('provider', ''),
            career_path=request.POST.get('career_path', 'other'),
            duration=request.POST.get('duration', ''),
            price=request.POST.get('price', 0),
            link=request.POST.get('link', ''),
            description=request.POST.get('description', ''),
        )
        course.save()  # type: ignore
        
        # Link course to guide
        guide_course = GuideCourse(
            guide=request.user,
            course=course
        )
        guide_course.save()
        
        messages.success(request, 'Course added successfully!')
        return redirect('manage_courses')
    
    return render(request, 'guide/add_course.html')

@login_required
def edit_course(request, course_id):
    # Check if user is a guide
    try:
        user_profile = get_object_or_404(RoleUser, user=request.user)
        if user_profile.role != 'guide':
            messages.error(request, 'Access denied. Guide access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if guide is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your guide account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get the course
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        # Update the course
        course.title = request.POST.get('title', course.title)
        course.provider = request.POST.get('provider', course.provider)
        course.career_path = request.POST.get('career_path', course.career_path)
        course.duration = request.POST.get('duration', course.duration)
        course.price = request.POST.get('price', course.price)
        course.link = request.POST.get('link', course.link)
        course.description = request.POST.get('description', course.description)
        course.save()
        
        messages.success(request, 'Course updated successfully!')
        return redirect('manage_courses')
    
    context = {
        'course': course,
    }
    return render(request, 'guide/edit_course.html', context)

@login_required
def delete_course(request, course_id):
    # Check if user is a guide
    try:
        user_profile = get_object_or_404(RoleUser, user=request.user)
        if user_profile.role != 'guide':
            messages.error(request, 'Access denied. Guide access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if guide is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your guide account is pending approval.')
        return redirect('admin_dashboard')
    
    # Get the course
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        # Delete the course
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('manage_courses')
    
    context = {
        'course': course,
    }
    return render(request, 'guide/delete_course.html', context)

@login_required
def create_post(request):
    # Check if user is a guide
    try:
        user_profile = get_object_or_404(RoleUser, user=request.user)
        if user_profile.role != 'guide':
            messages.error(request, 'Access denied. Guide access only.')
            return redirect('admin_dashboard')
    except Exception:
        messages.error(request, 'User profile not found.')
        return redirect('admin_dashboard')
    
    # Check if guide is approved
    if not user_profile.is_approved:
        messages.error(request, 'Your guide account is pending approval.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        # Create a feed post
        post = Post(
            author=request.user,
            content=request.POST.get('content', ''),
            post_type=request.POST.get('post_type', 'text'),
            media_url=request.POST.get('media_url', ''),
        )
        post.save()  # type: ignore
        
        messages.success(request, 'Post created successfully!')
        return redirect('guide_dashboard')
    
    return render(request, 'guide/create_post.html')

def guide_login(request):
    """View for guide login"""
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'guide/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is a guide
            try:
                from admin_panel.models import RoleUser
                user_profile = RoleUser.objects.get(user=user)
                
                if user_profile.role != 'guide':
                    messages.error(request, f'Access denied. This account is registered as {user_profile.role}, not a guide.')
                    return render(request, 'guide/login.html')
                
                if not user_profile.is_approved:
                    messages.warning(request, 'Your guide account is pending admin approval. Please wait for approval.')
                    return render(request, 'guide/login.html')
                
                # Everything is good, log them in
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('guide_dashboard')
                
            except RoleUser.DoesNotExist:
                messages.error(request, 'User profile not found. Please contact support.')
                return render(request, 'guide/login.html')
            except Exception as e:
                messages.error(request, f'Login error: {str(e)}')
                return render(request, 'guide/login.html')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'guide/login.html')


