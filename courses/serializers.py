from rest_framework import serializers
from .models import Course, SavedCourse

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'provider', 'career_path', 'duration', 'price', 'rating', 'link', 'description', 'is_certified', 'is_active', 'created_at']

class SavedCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = SavedCourse
        fields = ['id', 'course', 'saved_at']