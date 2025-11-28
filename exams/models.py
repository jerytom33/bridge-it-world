from django.db import models
from django.contrib.auth.models import User

class Exam(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=[
        ('10th', '10th'),
        ('12th', '12th'),
        ('ug', 'UG'),
        ('pg', 'PG'),
    ])
    last_date = models.DateField()
    link = models.URLField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'exams_exam'

class SavedExam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exam.title}"

    class Meta:
        db_table = 'exams_savedexam'
        unique_together = ('user', 'exam')