from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Course
from core.models import Profile
from core.utils import create_notification
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Course)
def notify_new_course(sender, instance, created, **kwargs):
    """
    Trigger notification when a new course is created.
    Notify all Student users.
    """
    if created and instance.is_active:
        try:
            # Notify all students
            # Filter users who have a profile with role='student'
            student_profiles = Profile.objects.filter(role='student')
            
            for profile in student_profiles:
                create_notification(
                    recipient=profile.user,
                    notification_type='new_course',
                    title=f"New Course: {instance.title}",
                    message=f"Check out the new course in {instance.career_path}: {instance.title}",
                    # related_post_id can be used for course ID here if frontend handles it
                    related_post_id=instance.id 
                )
        except Exception as e:
            logger.error(f"Error sending new course notification: {e}")
