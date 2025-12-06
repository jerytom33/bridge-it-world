import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

# Check which Exam model has data
print("=" * 60)
print("CHECKING DIFFERENT EXAM MODELS")
print("=" * 60)

try:
    from exams.models import Exam as ExamsExam
    exams_count = ExamsExam.objects.count()
    print(f"\n✓ exams.models.Exam: {exams_count} exams")
    if exams_count > 0:
        print("  Exams found:")
        for exam in ExamsExam.objects.all():
            print(f"    - {exam.title}")
except Exception as e:
    print(f"\n✗ exams.models.Exam error: {e}")

try:
    from bridge_core.models import Exam as BridgeExam
    bridge_count = BridgeExam.objects.count()
    print(f"\n✓ bridge_core.models.Exam: {bridge_count} exams")
except Exception as e:
    print(f"\n✗ bridge_core.models.Exam error: {e}")

try:
    from core.models import Exam as CoreExam
    core_count = CoreExam.objects.count()
    print(f"\n✓ core.models.Exam: {core_count} exams")
except Exception as e:
    print(f"\n✗ core.models.Exam error: {e}")

# Check Courses
print("\n" + "=" * 60)
print("CHECKING DIFFERENT COURSE MODELS")
print("=" * 60)

try:
    from courses.models import Course as CoursesCourse
    courses_count = CoursesCourse.objects.count()
    print(f"\n✓ courses.models.Course: {courses_count} courses")
    if courses_count > 0:
        print("  Courses found:")
        for course in CoursesCourse.objects.all():
            print(f"    - {course.title}")
except Exception as e:
    print(f"\n✗ courses.models.Course error: {e}")

try:
    from bridge_core.models import Course as BridgeCourse
    bridge_count = BridgeCourse.objects.count()
    print(f"\n✓ bridge_core.models.Course: {bridge_count} courses")
except Exception as e:
    print(f"\n✗ bridge_core.models.Course error: {e}")

try:
    from core.models import Course as CoreCourse
    core_count = CoreCourse.objects.count()
    print(f"\n✓ core.models.Course: {core_count} courses")
except Exception as e:
    print(f"\n✗ core.models.Course error: {e}")

print("\n" + "=" * 60)
