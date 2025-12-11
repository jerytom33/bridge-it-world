from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Exam, Notification


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


class NotificationSerializer(serializers.ModelSerializer):
    related_user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'title', 'message', 'is_read', 
                  'related_user', 'related_user_name', 'related_post_id', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_related_user_name(self, obj):
        if obj.related_user:
            return f"{obj.related_user.first_name} {obj.related_user.last_name}".strip() or obj.related_user.username
        return None


class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import FCMToken
        model = FCMToken
        fields = ['token', 'device_type']