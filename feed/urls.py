from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('posts/', views.FeedPostsView.as_view(), name='feed-posts'),
    path('posts/saved/', views.SavedPostsView.as_view(), name='saved-posts'),
    path('posts/liked/', views.LikedPostsView.as_view(), name='liked-posts'),
    path('posts/<int:pk>/like/', views.LikePostView.as_view(), name='post-like'),
    path('posts/<int:pk>/save/', views.SavePostView.as_view(), name='post-save'),
    path('posts/<int:pk>/view/', views.ViewPostView.as_view(), name='post-view'),
]