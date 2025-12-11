import os
import django
import sys

# Setup Django environment
sys.path.append(r'l:\ALTASH\bridge-it-world\bridge-it-world')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django: {e}")
    sys.exit(1)

from django.contrib.auth.models import User
from feed.models import Post, Like
from courses.models import Course
from core.models import Exam, Profile, Notification

def verify_signals():
    print("Verifying Real-Time Notification Signals...")
    
    # 1. Setup Test Users
    try:
        author = User.objects.get(username='rahul@gmail.com')
    except User.DoesNotExist:
        print("Test user 'rahul@gmail.com' not found. Please run setup_test_user.py first.")
        return

    # Create a secondary user for receiving notifications
    try:
        student_user, created = User.objects.get_or_create(username='student_test', email='student@test.com')
        if created:
            student_user.set_password('123456')
            student_user.save()
            Profile.objects.create(user=student_user, role='student')
            print("Created test student user 'student_test'")
    except Exception as e:
        print(f"Error creating student user: {e}")
        return

    # Clear previous notifications for clean test
    Notification.objects.filter(recipient=student_user).delete()
    Notification.objects.filter(recipient=author).delete()

    # 2. Test Feed Post Signal
    print("\n--- Testing Feed Post Signal ---")
    try:
        post = Post.objects.create(
            author=author,
            content="This is a test post for FCM signals.",
            post_type='text'
        )
        print(f"Created Post ID: {post.id}")
        
        # Check if student received notification
        notif = Notification.objects.filter(recipient=student_user, notification_type='new_post', related_post_id=post.id).first()
        if notif:
            print(f"SUCCESS: Notification created for student: {notif.title}")
        else:
            print("FAILURE: No notification found for student user.")
            
    except Exception as e:
        print(f"Feed Signal Error: {e}")

    # 3. Test Course Signal
    print("\n--- Testing Course Signal ---")
    try:
        course = Course.objects.create(
            title="Test FCM Course",
            provider="Udemy",
            career_path="software",
            duration="10 hours",
            price=19.99,
            link="http://example.com"
        )
        print(f"Created Course ID: {course.id}")
        
        # Check if student received notification
        notif = Notification.objects.filter(recipient=student_user, notification_type='new_course', related_post_id=course.id).first()
        if notif:
            print(f"SUCCESS: Notification created for student: {notif.title}")
        else:
            print("FAILURE: No notification found for student user.")
            
    except Exception as e:
        print(f"Course Signal Error: {e}")

    # 4. Test Like Signal
    print("\n--- Testing Like Signal ---")
    try:
        # Student likes Author's post
        Like.objects.create(user=student_user, post=post)
        print(f"Student liked Post ID: {post.id}")
        
        # Check if Author (rahul) received notification
        notif = Notification.objects.filter(recipient=author, notification_type='post_liked', related_post_id=post.id).first()
        if notif:
            print(f"SUCCESS: Notification created for author: {notif.title}")
        else:
            print("FAILURE: No notification found for author.")
            
    except Exception as e:
        print(f"Like Signal Error: {e}")

if __name__ == "__main__":
    verify_signals()
