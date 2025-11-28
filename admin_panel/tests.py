from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from bridge_core.models import UserProfile

class RegistrationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_guide_registration_page(self):
        """Test that the guide registration page loads correctly"""
        response = self.client.get(reverse('register_guide'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register as a Guide')
        
    def test_company_registration_page(self):
        """Test that the company registration page loads correctly"""
        response = self.client.get(reverse('register_company'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register as a Company')
        
    def test_guide_registration_submission(self):
        """Test guide registration form submission"""
        response = self.client.post(reverse('register_guide'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'username': 'johndoe',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        })
        
        # Check that the user was created
        self.assertTrue(User.objects.filter(username='johndoe').exists())
        
        # Check that the profile was created with correct role
        user = User.objects.get(username='johndoe')
        self.assertTrue(UserProfile.objects.filter(user=user, role='guide').exists())
        
        # Check that the user is not approved yet
        profile = UserProfile.objects.get(user=user)
        self.assertFalse(profile.is_approved)
        
    def test_company_registration_submission(self):
        """Test company registration form submission"""
        response = self.client.post(reverse('register_company'), {
            'company_name': 'Test Company',
            'contact_person': 'Jane Smith',
            'email': 'jane@testcompany.com',
            'username': 'testcompany',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        })
        
        # Check that the user was created
        self.assertTrue(User.objects.filter(username='testcompany').exists())
        
        # Check that the profile was created with correct role
        user = User.objects.get(username='testcompany')
        self.assertTrue(UserProfile.objects.filter(user=user, role='company').exists())
        
        # Check that the user is not approved yet
        profile = UserProfile.objects.get(user=user)
        self.assertFalse(profile.is_approved)