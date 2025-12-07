from django.db import models
from django.contrib.auth.models import User

class ResumeAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='resumes/')
    
    # Gemini AI Analysis (existing)
    gemini_response = models.JSONField(default=dict)
    
    # Resume Analyzer Module Results (new fields)
    candidate_name = models.CharField(max_length=255, blank=True)
    candidate_email = models.EmailField(blank=True)
    candidate_phone = models.CharField(max_length=50, blank=True)
    candidate_level = models.CharField(max_length=50, blank=True)  # Fresher/Intermediate/Experienced
    predicted_field = models.CharField(max_length=100, blank=True)  # Data Science, Web Dev, etc.
    resume_score = models.IntegerField(default=0)  # 0-100
    detected_skills = models.JSONField(default=list, blank=True)
    recommended_skills = models.JSONField(default=list, blank=True)
    recommended_courses = models.JSONField(default=list, blank=True)
    score_breakdown = models.JSONField(default=list, blank=True)
    analyzer_response = models.JSONField(default=dict, blank=True)  # Full analysis result
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Resume Analysis"

    class Meta:
        db_table = 'resume_resumeanalysis'
        ordering = ['-created_at']