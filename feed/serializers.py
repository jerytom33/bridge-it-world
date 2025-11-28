from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Like, Save

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'post_type', 'media_url', 'likes_count', 'comments_count', 'created_at', 'is_active', 'is_liked', 'is_saved', 'like_count']

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