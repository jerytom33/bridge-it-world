"""
API Demo Script

This script demonstrates how to use the BridgeIT API endpoints.
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def register_user(username, email, password):
    """Register a new user"""
    url = f"{BASE_URL}/auth/register/"
    data = {
        "username": username,
        "email": email,
        "password": password
    }
    response = requests.post(url, data=data)
    return response.json()

def login_user(username, password):
    """Login and get JWT token"""
    url = f"{BASE_URL}/token/"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=data)
    return response.json()

def get_current_user(token):
    """Get current user information"""
    url = f"{BASE_URL}/core/user/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def create_profile(token, profile_data):
    """Create a user profile"""
    url = f"{BASE_URL}/core/profile/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(profile_data))
    return response.json()

def get_profiles(token):
    """Get all profiles"""
    url = f"{BASE_URL}/core/profile/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def create_exam(token, exam_data):
    """Create an exam"""
    url = f"{BASE_URL}/core/exam/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(exam_data))
    return response.json()

def get_exams(token):
    """Get all exams"""
    url = f"{BASE_URL}/core/exam/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Example usage:
if __name__ == "__main__":
    print("BridgeIT API Demo")
    print("=" * 20)
    
    # Note: You would need to implement the actual registration endpoint
    # For now, we'll just show how to use the existing endpoints
    
    print("\n1. Login with the admin user:")
    print("   Username: admin")
    print("   Password: password")
    
    print("\n2. Use the token to access protected endpoints:")
    print("   - Get current user info")
    print("   - Create/view profiles")
    print("   - Create/view exams")
    
    print("\n3. Access bridge_core endpoints:")
    print("   - Career paths")
    print("   - Courses")
    print("   - Mentors")
    print("   - Mentorship sessions")
    print("   - Resources")
    
    print("\nExample API endpoints:")
    print(f"   GET  {BASE_URL}/core/user/ - Get current user")
    print(f"   POST {BASE_URL}/core/profile/ - Create profile")
    print(f"   GET  {BASE_URL}/core/profile/ - List profiles")
    print(f"   POST {BASE_URL}/core/exam/ - Create exam")
    print(f"   GET  {BASE_URL}/core/exam/ - List exams")
    print(f"   GET  {BASE_URL}/bridge/career-path/ - List career paths")
    print(f"   POST {BASE_URL}/bridge/course/ - Create course")