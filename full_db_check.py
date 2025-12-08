import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from bridge_core.models import Course, Exam
from admin_panel.models import RoleUser
from django.contrib.auth.models import User

print("=" * 70)
print("DATABASE CHECK - ALL DATA")
print("=" * 70)

# Check Courses
print("\n📚 COURSES:")
print("-" * 70)
courses = Course.objects.all()
print(f"Total: {courses.count()}")
if courses.exists():
    for i, course in enumerate(courses, 1):
        print(f"\n{i}. {course.title}")
        print(f"   ID: {course.id}")
        print(f"   Provider: {course.provider}")
        print(f"   Link: {course.link}")
else:
    print("❌ No courses found in bridge_core.models.Course")

# Check Exams
print("\n\n📝 EXAMS:")
print("-" * 70)
exams = Exam.objects.all()
print(f"Total: {exams.count()}")
if exams.exists():
    for i, exam in enumerate(exams, 1):
        print(f"\n{i}. {exam.title}")
        print(f"   ID: {exam.id}")
        print(f"   Category: {exam.category}")
        print(f"   Link: {exam.link}")
else:
    print("❌ No exams found in bridge_core.models.Exam")

# Check if admin user exists
print("\n\n👤 ADMIN USER:")
print("-" * 70)
try:
    admin_user = User.objects.get(username='admin')
    print(f"✅ Admin user exists")
    print(f"   Username: {admin_user.username}")
    print(f"   Is superuser: {admin_user.is_superuser}")
    print(f"   Is staff: {admin_user.is_staff}")
    print(f"   Is active: {admin_user.is_active}")
    
    # Check RoleUser for admin
    try:
        role = RoleUser.objects.get(user=admin_user)
        print(f"   Role: {role.role}")
        print(f"   Is approved: {role.is_approved}")
    except RoleUser.DoesNotExist:
        print(f"   No RoleUser profile (superuser doesn't need one)")
        
except User.DoesNotExist:
    print("❌ Admin user not found")

# Check other Course/Exam models
print("\n\n🔍 CHECKING FOR OTHER MODELS:")
print("-" * 70)
try:
    from core.models import Course as CoreCourse
    core_courses = CoreCourse.objects.all()
    print(f"✓ core.models.Course: {core_courses.count()} courses")
except:
    print("✗ core.models.Course not found or error")

try:
    from exams.models import Exam as ExamsCourse
    exams_exams = ExamsCourse.objects.all()
    print(f"✓ exams.models.Exam: {exams_exams.count()} exams")
except:
    print("✗ exams.models.Exam not found or error")

print("\n" + "=" * 70)
print("CONCLUSION:")
print("=" * 70)
if courses.count() == 0 and exams.count() == 0:
    print("❌ No data in bridge_core models")
    print("💡 Courses/Exams might be in a different app/model")
    print("   OR they need to be created")
else:
    print(f"✅ Found {courses.count()} courses and {exams.count()} exams")
    print("   These SHOULD appear in admin panel automatically")
print("=" * 70)
