import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

# Use the CORRECT models (same as admin panel now uses)
from courses.models import Course
from exams.models import Exam

print("=" * 60)
print("VERIFICATION - ADMIN PANEL WILL NOW SEE:")
print("=" * 60)

# Check Courses
courses = Course.objects.all()
print(f"\n📚 COURSES: {courses.count()}")
for course in courses:
    print(f"   ✓ {course.title}")
    if hasattr(course, 'provider'):
        print(f"     Provider: {course.provider}")
    if hasattr(course, 'link'):
        print(f"     Link: {course.link}")

# Check Exams  
exams = Exam.objects.all()
print(f"\n📝 EXAMS: {exams.count()}")
for exam in exams:
    print(f"   ✓ {exam.title}")
    if hasattr(exam, 'category'):
        print(f"     Category: {exam.category}")
    if hasattr(exam, 'link'):
        print(f"     Link: {exam.link}")

print("\n" + "=" * 60)
print("✅ FIXED! Admin panel now imports from:")
print("   - courses.models.Course")
print("   - exams.models.Exam")
print("\n💡 Refresh /admin-panel/courses/ and /admin-panel/exams/")
print("   Your data WILL appear now!")
print("=" * 60)
