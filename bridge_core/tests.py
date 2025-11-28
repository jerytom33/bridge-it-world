from django.test import TestCase
from django.contrib.auth.models import User
from .models import CareerPath, Course, Mentor


class BridgeCoreModelsTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testmentor',
            email='mentor@example.com',
            password='testpass123'
        )
        
        # Create a career path
        self.career_path = CareerPath.objects.create(
            title='Software Developer',
            description='Build applications and systems',
            education_level='ug',
            stream='Computer Science',
            skills_required=['Python', 'JavaScript', 'SQL'],
            avg_salary=75000.00,
            job_growth='High'
        )
        
        # Create a course
        self.course = Course.objects.create(
            title='Python for Beginners',
            description='Learn Python programming from scratch',
            provider='Online Academy',
            duration='3 months',
            price=99.99,
            career_path=self.career_path,
            link='https://example.com/python-course',
            rating=4.5,
            is_certified=True
        )
        
        # Create a mentor
        self.mentor = Mentor.objects.create(
            user=self.user,
            bio='Experienced software developer with 5 years in the industry',
            expertise=['Python', 'Django', 'React'],
            experience_years=5,
            company='Tech Corp',
            position='Senior Developer',
            linkedin_url='https://linkedin.com/in/testmentor',
            is_verified=True,
            rating=4.8
        )

    def test_career_path_creation(self):
        """Test that a career path can be created"""
        self.assertEqual(self.career_path.title, 'Software Developer')
        self.assertEqual(self.career_path.education_level, 'ug')
        
    def test_course_creation(self):
        """Test that a course can be created"""
        self.assertEqual(self.course.title, 'Python for Beginners')
        self.assertEqual(self.course.career_path, self.career_path)
        self.assertTrue(self.course.is_certified)
        
    def test_mentor_creation(self):
        """Test that a mentor can be created"""
        self.assertEqual(self.mentor.user.username, 'testmentor')
        self.assertEqual(self.mentor.company, 'Tech Corp')
        self.assertTrue(self.mentor.is_verified)