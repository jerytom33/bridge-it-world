from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

    class Meta:
        db_table = 'aptitude_question'

class UserAptitudeResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    answers = models.JSONField(default=dict)  # Store user's answers
    gemini_analysis = models.JSONField(default=dict)  # Store Gemini AI analysis
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}"

    class Meta:
        db_table = 'aptitude_useraptituderesult'
        ordering = ['-attempted_at']