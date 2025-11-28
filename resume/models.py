from django.db import models
from django.contrib.auth.models import User

class ResumeAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='resumes/')
    gemini_response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Resume Analysis"

    class Meta:
        db_table = 'resume_resumeanalysis'
        ordering = ['-created_at']