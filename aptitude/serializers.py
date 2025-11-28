from rest_framework import serializers
from .models import Question, UserAptitudeResult

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d']

class UserAptitudeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAptitudeResult
        fields = ['id', 'user', 'score', 'answers', 'gemini_analysis', 'attempted_at']
        read_only_fields = ['user', 'gemini_analysis', 'attempted_at']