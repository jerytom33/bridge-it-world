import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from django.contrib.auth.models import User
from admin_panel.models import RoleUser

try:
    user = User.objects.get(username='newguide')
    print(f"✅ User 'newguide' exists")
    print(f"   Email: {user.email}")
    print(f"   Active: {user.is_active}")
    
    # Check RoleUser
    try:
        role_user = RoleUser.objects.get(user=user)
        print(f"\n✅ RoleUser found!")
        print(f"   Role: {role_user.role}")
        print(f"   Approved: {role_user.is_approved}")
        print(f"   Phone: {role_user.phone}")
    except RoleUser.DoesNotExist:
        print(f"\n❌ NO RoleUser found for newguide!")
        print(f"   This is why login fails with 'User profile not found'")
        
        # Check all RoleUsers
        all_roles = RoleUser.objects.filter(user=user)
        print(f"\n   RoleUser count: {all_roles.count()}")
        
except User.DoesNotExist:
    print("❌ User 'newguide' does not exist")
