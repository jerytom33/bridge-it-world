from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    """User profile model for the core app."""
    
    # Type annotation to help static analysis tools
    objects = models.Manager()
    
    USER_ROLES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('guide', 'Guide'),
        ('company', 'Company')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='student')
    education_level = models.CharField(max_length=20, choices=[('10th', '10th'), ('12th', '12th'), ('UG', 'Undergraduate'), ('PG', 'Postgraduate')], blank=True)
    stream = models.CharField(max_length=100, blank=True)
    interests = models.JSONField(default=list)
    career_goals = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Exam(models.Model):
    """Exam model for tracking available exams."""
    
    # Type annotation to help static analysis tools
    objects = models.Manager()
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=20, choices=[('10th', '10th'), ('12th', '12th'), ('UG', 'Undergraduate'), ('PG', 'Postgraduate')])
    date = models.DateField()
    link = models.URLField(blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)  # type: ignore
    created_at = models.DateTimeField(default=timezone.now)