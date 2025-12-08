from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Post, Like, Save
from .serializers import PostSerializer

class FeedPostsView(generics.ListAPIView):
    """
    GET /api/feed/posts/
    Return all active posts with like/save status for the current user
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(is_active=True).select_related('author')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class LikePostView(APIView):
    """
    POST /api/feed/posts/<pk>/like/
    Like or unlike a post
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk, is_active=True)
        
        # Check if user already liked the post
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )
        
        if not created:
            # User already liked the post, so unlike it
            like.delete()
            # Decrement the likes count
            post.likes_count = max(0, post.likes_count - 1)
            post.save()
            return Response({
                'message': 'Post unliked successfully',
                'is_liked': False,
                'like_count': post.likes_count
            }, status=status.HTTP_200_OK)
        else:
            # User liked the post
            # Increment the likes count
            post.likes_count += 1
            post.save()
            
            # Notify post author if they are a company
            try:
                from admin_panel.models import RoleUser
                from core.utils import create_notification
                
                author_role = RoleUser.objects.filter(user=post.author, role='company').first()
                if author_role:
                    create_notification(
                        recipient=post.author,
                        notification_type='post_liked',
                        title='Someone Liked Your Post',
                        message=f'{request.user.get_full_name() or request.user.username} liked your post.',
                        related_user=request.user,
                        related_post_id=post.id
                    )
            except Exception as e:
                # Continue even if notification fails
                pass
            
            return Response({
                'message': 'Post liked successfully',
                'is_liked': True,
                'like_count': post.likes_count
            }, status=status.HTTP_201_CREATED)

class SavePostView(APIView):
    """
    POST /api/feed/posts/<pk>/save/
    Save or unsave a post
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk, is_active=True)
        
        # Check if user already saved the post
        save, created = Save.objects.get_or_create(
            user=request.user,
            post=post
        )
        
        if not created:
            # User already saved the post, so unsave it
            save.delete()
            return Response({
                'message': 'Post unsaved successfully',
                'is_saved': False
            }, status=status.HTTP_200_OK)
        else:
            # User saved the post
            
            # Notify post author if they are a company
            try:
                from admin_panel.models import RoleUser
                from core.utils import create_notification
                
                author_role = RoleUser.objects.filter(user=post.author, role='company').first()
                if author_role:
                    create_notification(
                        recipient=post.author,
                        notification_type='post_saved',
                        title='Someone Saved Your Post',
                        message=f'{request.user.get_full_name() or request.user.username} saved your post.',
                        related_user=request.user,
                        related_post_id=post.id
                    )
            except Exception as e:
                # Continue even if notification fails
                pass
            
            return Response({
                'message': 'Post saved successfully',
                'is_saved': True
            }, status=status.HTTP_201_CREATED)


class ViewPostView(APIView):
    """
    POST /api/feed/posts/<pk>/view/
    Track post view
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk, is_active=True)
        
        # Increment the views count
        post.views_count += 1
        post.save()
        
        return Response({
            'message': 'Post view tracked successfully',
            'view_count': post.views_count
        }, status=status.HTTP_200_OK)