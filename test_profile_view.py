import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from django.contrib.auth.models import User
from company.models import CompanyProfile

print("=" * 60)
print("TESTING COMPANY PROFILE VIEW LOGIC")
print("=" * 60)

# Test with user 'abc' who has complete data
try:
    user = User.objects.get(username='abc')
    print(f"\n✅ Found user: {user.username}")
    
    # Try to get company profile the same way the view does
    try:
        company_profile = CompanyProfile.objects.get(user=user)
        print(f"✅ CompanyProfile found!")
        print(f"\nProfile Data:")
        print(f"  Company Name: '{company_profile.company_name}'")
        print(f"  Description: '{company_profile.description}'")
        print(f"  Established: '{company_profile.established}'")
        print(f"  Employee Count: '{company_profile.employee_count}'")
        print(f"  Website: '{company_profile.website}'")
        print(f"  Industry: '{company_profile.industry}'")
        print(f"  Location: '{company_profile.location}'")
        print(f"  Contact Email: '{company_profile.contact_email}'")
        print(f"  Contact Phone: '{company_profile.contact_phone}'")
        
        # Check if any fields are None
        print(f"\n🔍 Field Type Check:")
        print(f"  established type: {type(company_profile.established)} = {company_profile.established}")
        print(f"  employee_count type: {type(company_profile.employee_count)} = {company_profile.employee_count}")
        
    except CompanyProfile.DoesNotExist:
        print("❌ CompanyProfile NOT FOUND using get()")
        
except User.DoesNotExist:
    print("❌ User 'abc' not found")

print("\n" + "=" * 60)
