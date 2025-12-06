import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from company.models import CompanyProfile
from admin_panel.models import RoleUser

print("=" * 60)
print("COMPANY PROFILE DATA CHECK")
print("=" * 60)

# Get all company profiles
profiles = CompanyProfile.objects.all()

if not profiles.exists():
    print("\n❌ No company profiles found!")
else:
    for profile in profiles:
        print(f"\n{'='*60}")
        print(f"👤 User: {profile.user.username}")
        print(f"🏢 Company Name: {profile.company_name or '(empty)'}")
        print(f"📝 Description: {(profile.description[:50] + '...') if profile.description else '(empty)'}")
        print(f"🌐 Website: {profile.website or '(empty)'}")
        print(f"🏭 Industry: {profile.industry or '(empty)'}")
        print(f"📅 Established: {profile.established or '(empty)'}")
        print(f"👥 Employees: {profile.employee_count or '(empty)'}")
        print(f"📍 Location: {profile.location or '(empty)'}")
        print(f"📧 Email: {profile.contact_email or '(empty)'}")
        print(f"📞 Phone: {profile.contact_phone or '(empty)'}")

print(f"\n{'='*60}")
