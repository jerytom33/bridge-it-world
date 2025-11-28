from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CareerPath(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    education_level = models.CharField(max_length=20, choices=[
        ('10th', '10th'), 
        ('12th', '12th'), 
        ('ug', 'UG'), 
        ('pg', 'PG')
    ])
    stream = models.CharField(max_length=100, blank=True)
    skills_required = models.JSONField(default=list)
    avg_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_growth = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    provider = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)  # e.g., "6 months", "2 years"
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    career_path = models.ForeignKey(CareerPath, on_delete=models.CASCADE, related_name='courses')
    link = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    is_certified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    expertise = models.JSONField(default=list)  # List of expertise areas
    experience_years = models.IntegerField(null=True, blank=True)
    company = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class MentorshipSession(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='sessions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorship_sessions')
    scheduled_time = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.mentor} - {self.student} on {self.scheduled_time}"


class Resource(models.Model):
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('book', 'Book'),
        ('tool', 'Tool'),
        ('website', 'Website'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    url = models.URLField()
    career_path = models.ForeignKey(CareerPath, on_delete=models.CASCADE, related_name='resources')
    author = models.CharField(max_length=100, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    is_free = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('guide', 'Guide'),
        ('company', 'Company'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)   # for guides & companies
    is_blocked = models.BooleanField(default=False)    # for all types
    # You can add: degree_level, interests, etc. later

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class CareerCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Stream(models.Model):
    name = models.CharField(max_length=100)
    career_category = models.ForeignKey(CareerCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ExamCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Exam(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(ExamCategory, on_delete=models.SET_NULL, null=True)
    level = models.CharField(max_length=20, choices=[
        ('10', '10th'),
        ('12', '12th'),
        ('ug', 'UG'),
        ('pg', 'PG'),
    ])
    last_date = models.DateField(null=True, blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title
