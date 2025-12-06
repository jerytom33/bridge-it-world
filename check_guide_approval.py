import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from admin_panel.models import RoleUser

print("=" * 60)
print("ALL GUIDES - APPROVAL STATUS")
print("=" * 60)

all_guides = RoleUser.objects.filter(role='guide')
pending = all_guides.filter(is_approved=False)
approved = all_guides.filter(is_approved=True)

print(f"\n📊 SUMMARY:")
print(f"   Total Guides: {all_guides.count()}")
print(f"   Pending Approval: {pending.count()}")
print(f"   Approved: {approved.count()}")

if pending.exists():
    print(f"\n⏳ PENDING GUIDES (Should appear in admin panel):")
    for guide in pending:
        print(f"   - {guide.user.username} ({guide.user.email})")
        print(f"     Approved: {guide.is_approved}")
else:
    print(f"\n✅ NO PENDING GUIDES")
    print(f"   All guides are already approved!")

if approved.exists():
    print(f"\n✅ APPROVED GUIDES:")
    for guide in approved:
        print(f"   - {guide.user.username} ({guide.user.email})")

print("\n" + "=" * 60)
print("💡 TIP:")
print("If you don't see pending guides in the admin panel,")
print("it's because they're all already approved!")
print("Check the 'Approved Guides' section (scroll down on the page)")
print("=" * 60)
