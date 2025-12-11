from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Exam, Profile
from .utils import create_notification
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Exam)
def notify_new_exam(sender, instance, created, **kwargs):
    """
    Trigger notification when a new exam is listed.
    Notify all Student users.
    """
    if created and instance.is_active:
        try:
            # Notify all students
            student_profiles = Profile.objects.filter(role='student')
            
            for profile in student_profiles:
                create_notification(
                    recipient=profile.user,
                    notification_type='new_exam',
                    title=f"New Exam Alert: {instance.title}",
                    message=f"A new exam has been listed: {instance.title}. Check details now.",
                    related_post_id=instance.id
                )
        except Exception as e:
            logger.error(f"Error sending new exam notification: {e}")
