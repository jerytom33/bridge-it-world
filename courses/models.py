from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=100)
    career_path = models.CharField(max_length=50, choices=[
        ('software', 'Software Engineering'),
        ('data', 'Data Science'),
        ('marketing', 'Digital Marketing'),
        ('finance', 'Finance'),
        ('other', 'Other'),
    ])
    duration = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    link = models.URLField()
    description = models.TextField()
    is_certified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to='thumbnails/courses/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'courses_course'

class SavedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    class Meta:
        db_table = 'courses_savedcourse'
        unique_together = ('user', 'course')