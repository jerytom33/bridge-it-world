from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Exam


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'education_level', 'stream', 'interests', 'career_goals', 'phone', 'created_at']
        read_only_fields = ['user']


class ExamSerializer(serializers.ModelSerializer):
    added_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'level', 'date', 'link', 'added_by', 'is_active', 'created_at']
        read_only_fields = ['added_by']