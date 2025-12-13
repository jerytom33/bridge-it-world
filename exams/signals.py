from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Exam
from core.utils import send_fcm_to_all

@receiver(post_save, sender=Exam)
def notify_new_exam(sender, instance, created, **kwargs):
    if created:
        print(f"📢 New Exam Created: {instance.title}")
        
        provider_name = "New Exam"
        if hasattr(instance, 'company') and instance.company:
            try:
                provider_name = instance.company.name
            except:
                pass
        elif hasattr(instance, 'guide') and instance.guide:
            try:
                if hasattr(instance.guide, 'user'):
                    provider_name = f"{instance.guide.user.first_name} {instance.guide.user.last_name}"
                else:
                    provider_name = "A Guide"
            except:
                provider_name = "A Guide"
                
        send_fcm_to_all(
             title=f"New Exam Alert: {instance.title}",
             body=f"{provider_name} has posted a new exam. Prepare now!",
             data={
                 "type": "new_exam",
                 "exam_id": str(instance.id),
                 "click_action": "FLUTTER_NOTIFICATION_CLICK"
             }
        )
