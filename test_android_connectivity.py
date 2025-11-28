import requests
import json

# Test the base URL
try:
    response = requests.get('http://192.168.220.3:8000/', timeout=5)
    print("Base URL test:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
except Exception as e:
    print(f"Base URL test failed: {e}")
    print()

# Test the signup endpoint
try:
    signup_data = {
        'username': 'androidtest',
        'email': 'android@test.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123',
        'first_name': 'Android',
        'last_name': 'Test'
    }
    response = requests.post('http://192.168.220.3:8000/api/auth/signup/', 
                           json=signup_data, 
                           timeout=10)
    print("Signup endpoint test:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
except Exception as e:
    print(f"Signup endpoint test failed: {e}")
    print()

# Test the login endpoint
try:
    login_data = {
        'username': 'androidtest',
        'password': 'testpass123'
    }
    response = requests.post('http://192.168.220.3:8000/api/auth/login/', 
                           json=login_data, 
                           timeout=10)
    print("Login endpoint test:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
except Exception as e:
    print(f"Login endpoint test failed: {e}")
    print()