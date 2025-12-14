from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Like, Save

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'avatar_url']
    
    def get_name(self, obj):
        return obj.get_full_name() or obj.username
    
    def get_avatar_url(self, obj):
        # Return None for now, implement if you add user avatars
        return None

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 
                 'like_count', 'is_liked', 'is_saved']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return Save.objects.filter(user=request.user, post=obj).exists()
        return False

    def get_like_count(self, obj):
        return obj.likes_count
    
    def get_title(self, obj):
        # Extract title from first line of content or first 50 chars
        content_lines = obj.content.strip().split('\n')
        if content_lines:
            return content_lines[0][:50]
        return obj.content[:50]