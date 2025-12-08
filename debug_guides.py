import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from django.contrib.auth.models import User
from admin_panel.models import RoleUser
from guide.models import GuideProfile

print("=" * 60)
print("GUIDE REGISTRATION & LOGIN DEBUG")
print("=" * 60)

# Find all guide users
guide_users = RoleUser.objects.filter(role='guide')
print(f"\n📊 Total Guide Users: {guide_users.count()}")

for role_user in guide_users:
    user = role_user.user
    print(f"\n{'='*60}")
    print(f"👤 Username: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Is Active: {user.is_active}")
    print(f"   Is Staff: {user.is_staff}")
    print(f"   Is Approved: {role_user.is_approved}")
    print(f"   Phone: {role_user.phone}")
    
    # Check if has GuideProfile
    try:
        guide_profile = GuideProfile.objects.get(user=user)
        print(f"✅ Has GuideProfile")
        print(f"   Bio: {(guide_profile.bio[:50] + '...') if guide_profile.bio else '(empty)'}")
        print(f"   Expertise: {guide_profile.expertise if hasattr(guide_profile, 'expertise') else 'N/A'}")
    except GuideProfile.DoesNotExist:
        print(f"❌ No GuideProfile found")
        print(f"   This guide CANNOT login to guide portal!")

    # Test if user can login
    print(f"\n🔐 Login Test:")
    if not user.is_active:
        print(f"   ❌ User account is INACTIVE - cannot login")
    elif not role_user.is_approved:
        print(f"   ⚠️  User NOT APPROVED - may not access guide portal")
    else:
        print(f"   ✅ User should be able to login")

print(f"\n{'='*60}")
