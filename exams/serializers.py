from rest_framework import serializers
from .models import Exam, SavedExam

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'title', 'category', 'level', 'last_date', 'link', 'description', 'is_active', 'created_at']

class SavedExamSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    
    class Meta:
        model = SavedExam
        fields = ['id', 'exam', 'saved_at']