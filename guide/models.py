from django.db import models
from django.contrib.auth.models import User
from bridge_core.models import UserProfile
from exams.models import Exam
from courses.models import Course
from feed.models import Post

class GuideProfile(models.Model):
    objects = models.Manager()  # Type hint for static analysis
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    expertise = models.JSONField(default=list)
    experience_years = models.IntegerField(null=True, blank=True)
    company = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Guide)"  # type: ignore

class GuideExam(models.Model):
    objects = models.Manager()  # Type hint for static analysis
    
    guide = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guide.username} - {self.exam.title}"  # type: ignore

class GuideCourse(models.Model):
    objects = models.Manager()  # Type hint for static analysis
    
    guide = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guide.username} - {self.course.title}"  # type: ignore

class GuidePost(models.Model):
    objects = models.Manager()  # Type hint for static analysis
    
    guide = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guide.username} - {self.post.content[:50]}"  # type: ignore