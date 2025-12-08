import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from bridge_core.models import Course, Exam

print("=" * 60)
print("ADDING SAMPLE DATA")
print("=" * 60)

# Add sample courses
courses_data = [
    {
        'title': 'Full Stack Web Development',
        'provider': 'Udemy',
        'career_path': 'software',
        'duration': '3 months',
        'price': 2999,
        'link': 'https://www.udemy.com/course/full-stack-web-development',
       'description': 'Learn HTML, CSS, JavaScript, React, Node.js and more'
    },
    {
        'title': 'Data Science Masterclass',
        'provider': 'Coursera',
        'career_path': 'data',
        'duration': '6 months',
        'price': 4999,
        'link': 'https://www.coursera.org/specializations/data-science',
        'description': 'Master Python, Machine Learning, and Data Analysis'
    },
    {
        'title': 'Digital Marketing Pro',
        'provider': 'Google Digital Garage',
        'career_path': 'marketing',
        'duration': '2 months',
        'price': 0,
        'link': 'https://learndigital.withgoogle.com',
        'description': 'SEO, Social Media Marketing, Google Ads fundamentals'
    }
]

print("\n📚 Creating Courses...")
for data in courses_data:
    course, created = Course.objects.get_or_create(
        title=data['title'],
        defaults=data
    )
    if created:
        print(f"  ✓ Created: {course.title}")
    else:
        print(f"  - Already exists: {course.title}")

# Add sample exams
exams_data = [
    {
        'title': 'JEE Main 2025',
        'category': 'Engineering',
        'level': 'UG',
        'last_date': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
        'link': 'https://jeemain.nta.nic.in',
        'description': 'Joint Entrance Examination for engineering admissions'
    },
    {
        'title': 'NEET 2025',
        'category': 'Medical',
        'level': 'UG',
        'last_date': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
        'link': 'https://neet.nta.nic.in',
        'description': 'National Eligibility cum Entrance Test for medical courses'
    },
    {
        'title': 'GATE 2025',
        'category': 'Engineering',
        'level': 'PG',
        'last_date': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
        'link': 'https://gate.iisc.ac.in',
        'description': 'Graduate Aptitude Test in Engineering for PG admissions'
    }
]

print("\n📝 Creating Exams...")
for data in exams_data:
    exam, created = Exam.objects.get_or_create(
        title=data['title'],
        defaults=data
    )
    if created:
        print(f"  ✓ Created: {exam.title}")
    else:
        print(f"  - Already exists: {exam.title}")

print("\n" + "=" * 60)
print("✅ SAMPLE DATA ADDED!")
print(f"   Courses: {Course.objects.count()}")
print(f"   Exams: {Exam.objects.count()}")
print("=" * 60)
print("\n💡 Now refresh your browser:")
print("   - /admin-panel/courses/ → Shows 3 courses")
print("   - /admin-panel/exams/ → Shows 3 exams")
print("=" * 60)
