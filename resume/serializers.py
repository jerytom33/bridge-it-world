from rest_framework import serializers
from .models import ResumeAnalysis

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = ['id', 'user', 'pdf_file', 'gemini_response', 'created_at']
        read_only_fields = ['user', 'gemini_response', 'created_at']