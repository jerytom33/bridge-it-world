import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from bridge_core.models import Course, Exam

print("=" * 60)
print("DATABASE DATA CHECK")
print("=" * 60)

# Check Courses
courses_count = Course.objects.count()
print(f"\n📚 COURSES: {courses_count} total")
if courses_count > 0:
    print("\nFirst 3 courses:")
    for course in Course.objects.all()[:3]:
        print(f"  - {course.title} by {course.provider}")

# Check Exams
exams_count = Exam.objects.count()
print(f"\n📝 EXAMS: {exams_count} total")
if exams_count > 0:
    print("\nFirst 3 exams:")
    for exam in Exam.objects.all()[:3]:
        print(f"  - {exam.title} ({exam.category})")

print("\n" + "=" * 60)
print("VERIFICATION:")
print(f"✓ Courses and Exams are {'DIFFERENT' if courses_count != exams_count else 'SAME COUNT'}")
print("=" * 60)
