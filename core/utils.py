import google.generativeai as genai
import os
import logging
import json
import firebase_admin
from firebase_admin import credentials, messaging

logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK
# Path to service account key
SERVICE_ACCOUNT_KEY = r"L:\ALTASH\bridge-it-world\bridge-it-world\firebase\bridge-it-world-firebase-adminsdk-fbsvc-39ef5e20e0.json"
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin SDK: {e}")

def call_gemini_api(prompt):
    """
    Reusable function to call Gemini API with error handling
    """
    try:
        # Configure Gemini API key  
        api_key = os.environ.get('GEMINI_API_KEY')
        
        if not api_key:
            print("DEBUG: GEMINI_API_KEY not found in environment")
            return "Error: AI service not configured (Missing API Key)"
            
        genai.configure(api_key=api_key)
        
        # Try multiple model names in order of preference
        models_to_try = [
            'gemini-2.5-flash',
            'gemini-2.0-flash',
            'gemini-flash-latest',
        ]
        
        last_error = None
        for model_name in models_to_try:
            try:
                # Create the model
                model = genai.GenerativeModel(model_name)
                
                # Generate content
                response = model.generate_content(prompt)
                
                logger.info(f"Successfully used model: {model_name}")
                return response.text
            
            except Exception as e:
                last_error = e
                logger.warning(f"Model {model_name} failed: {str(e)}")
                continue
        
        # If all models failed, raise the last error
        raise last_error if last_error else Exception("All model attempts failed")
    
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Gemini API Error: {str(e)}")
        
        # Return a JSON error response instead of dict
        error_response = {
            "error": "AI service temporarily unavailable",
            "details": str(e),
            "suitable_career_paths": ["Unable to analyze at this time"],
            "skill_gaps": [],
            "recommended_courses": [],
            "suggested_next_steps": ["Please try again later"],
            "overall_summary": "Analysis unavailable due to AI service error"
        }
        return json.dumps(error_response)


# Notification Helper Functions
def create_notification(recipient, notification_type, title, message, related_user=None, related_post_id=None):
    """
    Create a notification for a specific user and send push notification via FCM.
    
    Args:
        recipient: User object who will receive the notification
        notification_type: Type of notification (from Notification.NOTIFICATION_TYPES)
        title: Notification title
        message: Notification message
        related_user: Optional User object related to the notification
        related_post_id: Optional post ID related to the notification
    
    Returns:
        Notification object
    """
    from core.models import Notification, FCMToken
    
    # 1. Create Database Notification
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        related_user=related_user,
        related_post_id=related_post_id
    )
    
    # 2. Send FCM Push Notification
    try:
        # Get all active tokens for the user
        fcm_tokens = FCMToken.objects.filter(user=recipient).values_list('token', flat=True)
        
        if fcm_tokens:
            # Create a message to send to all devices
            # Note: For simplicity, sending individual messages, but could use multicast for efficiency
            for token in fcm_tokens:
                try:
                    fcm_message = messaging.Message(
                        notification=messaging.Notification(
                            title=title,
                            body=message,
                        ),
                        data={
                            'type': notification_type,
                            'notification_id': str(notification.id),
                            'related_post_id': str(related_post_id) if related_post_id else "",
                        },
                        token=token,
                    )
                    response = messaging.send(fcm_message)
                    logger.info(f"Successfully sent message to token {token[:10]}...: {response}")
                except Exception as e:
                    logger.warning(f"Failed to send FCM message to token {token[:10]}...: {e}")
                    # Optional: Delete invalid tokens here
    except Exception as e:
        logger.error(f"Error in FCM notification process: {e}")
    
    return notification


def notify_all_admins(notification_type, title, message, related_user=None, related_post_id=None):
    """
    Create notifications for all admin users.
    
    Args:
        notification_type: Type of notification
        title: Notification title
        message: Notification message
        related_user: Optional User object related to the notification
        related_post_id: Optional post ID related to the notification
    
    Returns:
        List of created Notification objects
    """
    from django.contrib.auth.models import User
    from admin_panel.models import RoleUser
    
    notifications = []
    try:
        # Get all admin users
        admin_role_users = RoleUser.objects.filter(role='admin')
        
        for role_user in admin_role_users:
            notification = create_notification(
                recipient=role_user.user,
                notification_type=notification_type,
                title=title,
                message=message,
                related_user=related_user,
                related_post_id=related_post_id
            )
            notifications.append(notification)
    except Exception as e:
        print(f"Error notifying admins: {str(e)}")
    
    
    return notifications

def send_fcm_to_all(title, body, data=None):
    """
    Send FCM notification to all users (subscribed to 'all_users' topic)
    """
    try:
        # Create message for 'all_users' topic
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            topic='all_users',
        )
        
        # Send message
        response = messaging.send(message)
        logger.info(f"Successfully sent FCM broadcast to 'all_users': {response}")
        return response
        
    except Exception as e:
        logger.error(f"Error sending FCM broadcast: {e}")
        return None
