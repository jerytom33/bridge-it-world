from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post, Like
from core.utils import create_notification
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Post)
def notify_new_post(sender, instance, created, **kwargs):
    """
    Trigger notification when a new post is created.
    Notify all users except the author.
    """
    if created and instance.is_active:
        try:
            # Notify all users except author
            # Note: For large scale, this should use a task queue
            users = User.objects.exclude(id=instance.author.id)
            
            for user in users:
                create_notification(
                    recipient=user,
                    notification_type='new_post',
                    title=f"New Post from {instance.author.username}",
                    message=f"{instance.content[:50]}...",
                    related_user=instance.author,
                    related_post_id=instance.id
                )
        except Exception as e:
            logger.error(f"Error sending new post notification: {e}")

@receiver(post_save, sender=Like)
def notify_post_like(sender, instance, created, **kwargs):
    """
    Trigger notification when a user likes a post.
    Notify the post author.
    """
    if created:
        try:
            # Don't notify if user likes their own post
            if instance.user != instance.post.author:
                create_notification(
                    recipient=instance.post.author,
                    notification_type='post_liked',
                    title="New Like",
                    message=f"{instance.user.username} liked your post",
                    related_user=instance.user,
                    related_post_id=instance.post.id
                )
        except Exception as e:
            logger.error(f"Error sending like notification: {e}")
