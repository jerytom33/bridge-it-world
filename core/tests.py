from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Exam


class CoreModelsTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a profile for the user
        self.profile = Profile.objects.create(
            user=self.user,
            role='student',
            education_level='ug',
            stream='Computer Science',
            interests=['programming', 'web development'],
            career_goals='Become a software developer',
            phone='1234567890'
        )
        
        # Create an exam
        self.exam = Exam.objects.create(
            title='Python Certification Exam',
            description='Test your Python skills',
            level='ug',
            date='2025-12-01',
            link='https://example.com/exam',
            added_by=self.user,
            is_active=True
        )

    def test_profile_creation(self):
        """Test that a profile can be created"""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.role, 'student')
        self.assertEqual(self.profile.education_level, 'ug')
        
    def test_exam_creation(self):
        """Test that an exam can be created"""
        self.assertEqual(self.exam.title, 'Python Certification Exam')
        self.assertEqual(self.exam.added_by, self.user)
        self.assertTrue(self.exam.is_active)
        
    def test_user_profile_relationship(self):
        """Test the relationship between User and Profile"""
        self.assertEqual(self.user.profile, self.profile)