import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from django.contrib.auth.models import User
from admin_panel.models import RoleUser
from guide.models import GuideProfile

print("=" * 60)
print("CREATING NEW UNAPPROVED GUIDE")
print("=" * 60)

username = "newguide"
password = "test123"
email = "newguide@example.com"

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"\n❌ User '{username}' already exists!")
    # Delete and recreate
    user = User.objects.get(username=username)
    print(f"   Deleting existing user and recreating...")
    user.delete()

# Create user
user = User.objects.create_user(
    username=username,
    email=email,
    password=password,
    first_name="New",
    last_name="Guide"
)

# Create RoleUser with is_approved=False
role_user = RoleUser.objects.create(
    user=user,
    role='guide',
    is_approved=False,  # NOT APPROVED
    phone="9876543210"
)

# Create GuideProfile
guide_profile = GuideProfile.objects.create(
    user=user,
    bio="This is a new guide pending approval for testing purposes.",
    expertise=["Career Counselling", "Technical Guidance"],
    experience_years=3,
    company="Test Company Ltd",
    position="Career Guide",
    linkedin_url="https://linkedin.com/in/newguide"
)

print(f"\n✅ Successfully created new UNAPPROVED guide!")
print(f"\n📝 Guide Details:")
print(f"   Username: {username}")
print(f"   Password: {password}")
print(f"   Email: {email}")
print(f"   Is Approved: {role_user.is_approved} ⚠️ (Should be False)")
print(f"   Role: {role_user.role}")
print(f"   Phone: {role_user.phone}")

print(f"\n✅ Guide Profile Created:")
print(f"   Bio: {guide_profile.bio[:50]}...")
print(f"   Expertise: {guide_profile.expertise}")
print(f"   Experience: {guide_profile.experience_years} years")

print(f"\n📋 Testing Instructions:")
print(f"   1. Login as admin at /accounts/login/")
print(f"   2. Go to /admin-panel/guides-companies/")
print(f"   3. Look in 'Pending Guide Approvals' section")
print(f"   4. You should see '{username}' (New Guide)")
print(f"   5. Click 'Approve' to approve")
print(f"\n   6. After approval, try logging in at /guide/login/:")
print(f"      Username: {username}")
print(f"      Password: {password}")

print("\n" + "=" * 60)
