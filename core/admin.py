from django.contrib import admin
from .models import Profile, Exam  # Add more later

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'education_level']

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'date']