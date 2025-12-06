import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from bridge_core.models import Exam

print("=" * 60)
print("CHECKING EXAMS IN DATABASE")
print("=" * 60)

exams = Exam.objects.all()
print(f"\n📝 Total Exams: {exams.count()}")

if exams.exists():
    print("\nExams found:")
    for i, exam in enumerate(exams, 1):
        print(f"\n{i}. {exam.title}")
        print(f"   Category: {exam.category}")
        print(f"   Level: {exam.level}")
        print(f"   Last Date: {exam.last_date}")
        print(f"   Link: {exam.link or 'N/A'}")
else:
    print("\n❌ No exams in database")
    print("\n💡 The admin panel will show 'No exams available'")
    print("   Exams are added by Guides, not Admin")

print("\n" + "=" * 60)
print("✅ The view automatically displays all exams from database")
print("   Any exams added will appear immediately!")
print("=" * 60)
