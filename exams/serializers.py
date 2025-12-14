from rest_framework import serializers
from .models import Exam, SavedExam

class ExamSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'category', 'level', 'last_date', 'link', 
                 'description', 'is_active', 'created_at', 'image', 'is_saved']
    
    def get_image(self, obj):
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
        return None
    
    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return SavedExam.objects.filter(user=request.user, exam=obj).exists()
        return False

class SavedExamSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    
    class Meta:
        model = SavedExam
        fields = ['id', 'exam', 'saved_at']