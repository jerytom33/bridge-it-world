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
    thumbnail = models.ImageField(upload_to='thumbnails/exams/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)


class Notification(models.Model):
    """Notification model for system-wide notifications."""
    
    # Type annotation to help static analysis tools
    objects = models.Manager()
    
    NOTIFICATION_TYPES = [
        ('user_registration', 'User Registration'),
        ('guide_registration', 'Guide Registration Pending'),
        ('company_registration', 'Company Registration Pending'),
        ('guide_approved', 'Guide Approved'),
        ('guide_rejected', 'Guide Rejected'),
        ('company_approved', 'Company Approved'),
        ('company_rejected', 'Company Rejected'),
        ('guide_logout', 'Guide Logged Out'),
        ('post_liked', 'Post Liked'),
        ('post_saved', 'Post Saved'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # type: ignore
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='related_notifications')
    related_post_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'core_notification'
    
    def __str__(self):
        return f"{self.recipient.username} - {self.title}"


class FCMToken(models.Model):
    """Model to store FCM tokens for push notifications."""
    
    # Type annotation to help static analysis tools
    objects = models.Manager()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fcm_tokens')
    token = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=20, default='android')
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'core_fcm_token'
        ordering = ['-last_used']
    
    def __str__(self):
        return f"{self.user.username} - {self.device_type} - {self.token[:10]}..."
