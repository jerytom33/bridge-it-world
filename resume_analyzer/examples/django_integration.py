"""
Django Integration Example for Resume Analyzer

This example shows how to integrate the resume_analyzer module into a Django project.
"""

# ============================================
# models.py
# ============================================

from django.db import models
from django.contrib.auth.models import User

class ResumeAnalysis(models.Model):
    """Model to store resume analysis results."""
    
    # User who uploaded the resume (optional)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # File and basic info
    resume_file = models.FileField(upload_to='resumes/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Extracted basic details
    candidate_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    mobile_number = models.CharField(max_length=50, blank=True)
    
    # Analysis results
    candidate_level = models.CharField(max_length=50, blank=True)  # Fresher, Intermediate, Experienced
    predicted_field = models.CharField(max_length=100, blank=True)  # Data Science, Web Dev, etc.
    resume_score = models.IntegerField(default=0)
    
    # JSON fields for detailed data
    detected_skills = models.JSONField(default=list, blank=True)
    recommended_skills = models.JSONField(default=list, blank=True)
    recommended_courses = models.JSONField(default=list, blank=True)
    score_breakdown = models.JSONField(default=list, blank=True)
    full_analysis = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Resume Analysis'
        verbose_name_plural = 'Resume Analyses'
    
    def __str__(self):
        return f"{self.candidate_name or 'Unknown'} - {self.resume_score}/100 - {self.uploaded_at.strftime('%Y-%m-%d')}"


# ============================================
# views.py
# ============================================

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from resume_analyzer import analyze_resume
import os
import tempfile

@login_required
def upload_resume_view(request):
    """View for uploading and analyzing a resume."""
    
    if request.method == 'POST' and request.FILES.get('resume'):
        resume_file = request.FILES['resume']
        
        # Validate file type
        if not resume_file.name.endswith('.pdf'):
            return JsonResponse({
                'success': False,
                'error': 'Only PDF files are supported'
            }, status=400)
        
        # Save file temporarily for analysis
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            for chunk in resume_file.chunks():
                tmp_file.write(chunk)
            temp_path = tmp_file.name
        
        try:
            # Analyze the resume
            result = analyze_resume(temp_path)
            
            # Save to database
            from .models import ResumeAnalysis
            analysis = ResumeAnalysis.objects.create(
                user=request.user,
                resume_file=resume_file,
                candidate_name=result['basic_details'].get('name', ''),
                email=result['basic_details'].get('email', ''),
                mobile_number=result['basic_details'].get('mobile_number', ''),
                candidate_level=result['candidate_level'],
                predicted_field=result['predicted_field'],
                resume_score=result['resume_score'],
                detected_skills=result['basic_details'].get('skills', []),
                recommended_skills=result['recommended_skills'],
                recommended_courses=result['recommended_courses'],
                score_breakdown=result['score_breakdown'],
                full_analysis=result
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # AJAX request
                return JsonResponse({
                    'success': True,
                    'analysis_id': analysis.id,
                    'result': result
                })
            else:
                # Regular form submission
                return redirect('resume_detail', pk=analysis.id)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    return render(request, 'resume/upload.html')


@login_required
def resume_detail_view(request, pk):
    """View to display resume analysis details."""
    from .models import ResumeAnalysis
    
    analysis = get_object_or_404(ResumeAnalysis, pk=pk, user=request.user)
    
    context = {
        'analysis': analysis,
    }
    
    return render(request, 'resume/detail.html', context)


@login_required
def resume_list_view(request):
    """View to list all resume analyses for the logged-in user."""
    from .models import ResumeAnalysis
    
    analyses = ResumeAnalysis.objects.filter(user=request.user)
    
    context = {
        'analyses': analyses,
    }
    
    return render(request, 'resume/list.html', context)


# ============================================
# urls.py
# ============================================

from django.urls import path
from . import views

app_name = 'resume'

urlpatterns = [
    path('upload/', views.upload_resume_view, name='upload'),
    path('detail/<int:pk>/', views.resume_detail_view, name='detail'),
    path('list/', views.resume_list_view, name='list'),
]


# ============================================
# admin.py
# ============================================

from django.contrib import admin
from .models import ResumeAnalysis

@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ['candidate_name', 'email', 'predicted_field', 'resume_score', 'candidate_level', 'uploaded_at']
    list_filter = ['predicted_field', 'candidate_level', 'uploaded_at']
    search_fields = ['candidate_name', 'email', 'mobile_number']
    readonly_fields = ['uploaded_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'resume_file', 'uploaded_at')
        }),
        ('Contact Details', {
            'fields': ('candidate_name', 'email', 'mobile_number')
        }),
        ('Analysis Results', {
            'fields': ('candidate_level', 'predicted_field', 'resume_score')
        }),
        ('Skills', {
            'fields': ('detected_skills', 'recommended_skills')
        }),
        ('Recommendations', {
            'fields': ('recommended_courses', 'score_breakdown')
        }),
        ('Full Analysis Data', {
            'fields': ('full_analysis',),
            'classes': ('collapse',)
        }),
    )


# ============================================
# Example Template: templates/resume/upload.html
# ============================================
"""
<!DOCTYPE html>
<html>
<head>
    <title>Upload Resume</title>
</head>
<body>
    <h1>Upload Your Resume</h1>
    
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <div>
            <label for="resume">Select Resume (PDF only):</label>
            <input type="file" name="resume" id="resume" accept=".pdf" required>
        </div>
        <button type="submit">Analyze Resume</button>
    </form>
    
    <p><a href="{% url 'resume:list' %}">View My Analyses</a></p>
</body>
</html>
"""


# ============================================
# Example Template: templates/resume/detail.html
# ============================================
"""
<!DOCTYPE html>
<html>
<head>
    <title>Resume Analysis - {{ analysis.candidate_name }}</title>
</head>
<body>
    <h1>Resume Analysis Results</h1>
    
    <h2>Basic Information</h2>
    <p><strong>Name:</strong> {{ analysis.candidate_name }}</p>
    <p><strong>Email:</strong> {{ analysis.email }}</p>
    <p><strong>Phone:</strong> {{ analysis.mobile_number }}</p>
    
    <h2>Analysis Results</h2>
    <p><strong>Experience Level:</strong> {{ analysis.candidate_level }}</p>
    <p><strong>Predicted Field:</strong> {{ analysis.predicted_field }}</p>
    <p><strong>Resume Score:</strong> {{ analysis.resume_score }}/100</p>
    
    <h2>Detected Skills</h2>
    <ul>
        {% for skill in analysis.detected_skills %}
            <li>{{ skill }}</li>
        {% endfor %}
    </ul>
    
    <h2>Recommended Skills</h2>
    <ul>
        {% for skill in analysis.recommended_skills %}
            <li>{{ skill }}</li>
        {% endfor %}
    </ul>
    
    <h2>Score Breakdown</h2>
    <ul>
        {% for item in analysis.score_breakdown %}
            <li>{{ item }}</li>
        {% endfor %}
    </ul>
    
    <h2>Recommended Courses</h2>
    <ul>
        {% for course in analysis.recommended_courses %}
            <li><a href="{{ course.link }}" target="_blank">{{ course.name }}</a></li>
        {% endfor %}
    </ul>
    
    <p><a href="{% url 'resume:list' %}">Back to List</a></p>
</body>
</html>
"""
