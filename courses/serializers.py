from rest_framework import serializers
from .models import Course, SavedCourse

class CourseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'provider', 'career_path', 'duration', 'price', 
                 'rating', 'link', 'description', 'is_certified', 'is_active', 
                 'created_at', 'image', 'is_saved']
    
    def get_image(self, obj):
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
        return None
    
    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return SavedCourse.objects.filter(user=request.user, course=obj).exists()
        return False

class SavedCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = SavedCourse
        fields = ['id', 'course', 'saved_at']