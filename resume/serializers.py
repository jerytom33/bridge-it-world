from rest_framework import serializers
from .models import ResumeAnalysis

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = [
            'id', 'user', 'pdf_file', 
            'gemini_response',  # Existing Gemini data
            # New analyzer fields
            'candidate_name', 'candidate_email', 'candidate_phone',
            'candidate_level', 'predicted_field', 'resume_score',
            'detected_skills', 'recommended_skills', 'recommended_courses',
            'score_breakdown', 'analyzer_response',
            'created_at'
        ]
        read_only_fields = ['user', 'gemini_response', 'created_at']