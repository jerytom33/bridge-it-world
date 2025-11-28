from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CareerPath, Course, Mentor, MentorshipSession, Resource


class CareerPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerPath
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    career_path = CareerPathSerializer(read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'


class MentorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class MentorSerializer(serializers.ModelSerializer):
    user = MentorUserSerializer(read_only=True)
    
    class Meta:
        model = Mentor
        fields = '__all__'
        read_only_fields = ['user']


class MentorshipSessionSerializer(serializers.ModelSerializer):
    mentor = MentorSerializer(read_only=True)
    student = MentorUserSerializer(read_only=True)
    
    class Meta:
        model = MentorshipSession
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    career_path = CareerPathSerializer(read_only=True)
    
    class Meta:
        model = Resource
        fields = '__all__'