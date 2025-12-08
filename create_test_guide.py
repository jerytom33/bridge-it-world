import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from django.contrib.auth.models import User
from admin_panel.models import RoleUser
from guide.models import GuideProfile

print("=" * 60)
print("CREATING TEST UNAPPROVED GUIDE")
print("=" * 60)

# Create a new test guide that's NOT approved
username = "testguide"
password = "test123"

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"\n❌ User '{username}' already exists!")
    print("Please login as admin and delete this user first, or use a different username.")
else:
    # Create user
    user = User.objects.create_user(
        username=username,
        email="testguide@example.com",
        password=password,
        first_name="Test",
        last_name="Guide"
    )
    
    # Create RoleUser with is_approved=False
    role_user = RoleUser.objects.create(
        user=user,
        role='guide',
        is_approved=False,  # NOT APPROVED - will show in pending
        phone="1234567890"
    )
    
    # Create GuideProfile
    guide_profile = GuideProfile.objects.create(
        user=user,
        bio="Test guide for approval testing",
        expertise=["Career Counselling", "Test"],
        experience_years=5,
        company="Test Company",
        position="Senior Guide",
        linkedin_url="https://linkedin.com/in/testguide"
    )
    
    print(f"\n✅ Created test guide successfully!")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"   Email: testguide@example.com")
    print(f"   Approved: {role_user.is_approved} (Should be False)")
    print(f"\n📋 Next Steps:")
    print(f"   1. Go to /admin-panel/guides-companies/")
    print(f"   2. You should see '{username}' in 'Pending Guide Approvals'")
    print(f"   3. Click 'Approve' to approve the guide")
    print(f"   4. Try logging in at /guide/login/ with:")
    print(f"      Username: {username}")
    print(f"      Password: {password}")

print("\n" + "=" * 60)
