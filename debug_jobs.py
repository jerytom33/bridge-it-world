import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from django.contrib.auth.models import User
from company.models import CompanyProfile, JobPosting
from admin_panel.models import RoleUser

# Debug script to check job postings visibility

print("=" * 60)
print("JOB POSTINGS DEBUG SCRIPT")
print("=" * 60)

# Find companies
companies = User.objects.filter(roleuser__role='company')
print(f"\n📊 Total Companies: {companies.count()}")

for user in companies:
    print(f"\n{'='*60}")
    print(f"👤 Username: {user.username}")
    print(f"   Email: {user.email}")
    
    # Check if has company profile
    try:
        profile = CompanyProfile.objects.get(user=user)
        print(f"✅ Has CompanyProfile: {profile.company_name}")
        print(f"   Profile ID: {profile.id}")
        
        # Check jobs linked to this profile
        jobs_by_profile = JobPosting.objects.filter(company=profile)
        print(f"\n📋 Jobs linked to profile: {jobs_by_profile.count()}")
        for job in jobs_by_profile:
            print(f"   - {job.title} (ID: {job.id}, Created: {job.created_at})")
        
        # Check jobs by user (the query used in views)
        jobs_by_user = JobPosting.objects.filter(company__user=user)
        print(f"\n📋 Jobs by company__user query: {jobs_by_user.count()}")
        for job in jobs_by_user:
            print(f"   - {job.title} (ID: {job.id})")
            
    except CompanyProfile.DoesNotExist:
        print("❌ No CompanyProfile found")
        print("   This user CANNOT create jobs without a profile!")

print(f"\n{'='*60}")
print(f"📊 Total JobPostings in database: {JobPosting.objects.count()}")
all_jobs = JobPosting.objects.all()
for job in all_jobs:
    print(f"   - {job.title}")
    print(f"     Company: {job.company.company_name if job.company else 'None'}")
    print(f"     User: {job.company.user.username if job.company and job.company.user else 'None'}")
print("=" * 60)
