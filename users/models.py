from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    LEVEL_CHOICES = [
        ('10th', '10th'),
        ('12th', '12th'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # New fields required for Bridge it
    current_level = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True)
    stream = models.CharField(max_length=100, blank=True)
    interests = models.JSONField(default=list, blank=True)  # e.g. ["Coding", "Design"]
    career_goals = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"