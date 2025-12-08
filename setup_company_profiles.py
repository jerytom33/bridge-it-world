import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from django.contrib.auth.models import User
from company.models import CompanyProfile
from admin_panel.models import RoleUser

print("=" * 60)
print("COMPANY PROFILE SETUP SCRIPT")
print("=" * 60)

# Find all company users
company_users = RoleUser.objects.filter(role='company', is_approved=True)

if not company_users.exists():
    print("\n❌ No approved company users found!")
    print("\nPlease make sure you have:")
    print("1. Registered a company via /admin-panel/register-company/")
    print("2. Approved the company via /admin-panel/guides-companies/")
else:
    for role_user in company_users:
        user = role_user.user
        print(f"\n{'='*60}")
        print(f"👤 Company User: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Approved: {role_user.is_approved}")
        
        # Check if profile exists
        try:
            profile = CompanyProfile.objects.get(user=user)
            print(f"✅ CompanyProfile already exists!")
            print(f"   Company Name: {profile.company_name}")
        except CompanyProfile.DoesNotExist:
            print(f"⚠️  No CompanyProfile found. Creating one...")
            
            # Create a basic profile
            profile = CompanyProfile.objects.create(
                user=user,
                company_name=user.first_name or f"{user.username}'s Company",
                description="Welcome to our company! Please update your profile.",
                industry="Technology",
                location="Not Specified",
                contact_email=user.email,
                contact_phone=role_user.phone or ""
            )
            print(f"✅ CompanyProfile created!")
            print(f"   Company Name: {profile.company_name}")
            print(f"\n💡 NOTE: Please update your profile at /company/profile/update/")

print(f"\n{'='*60}")
print("✅ Setup complete!")
print("\nYou can now:")
print("1. Login at /company/login/")
print("2. Update profile at /company/profile/update/")
print("3. Create jobs at /company/jobs/create/")
print("=" * 60)
