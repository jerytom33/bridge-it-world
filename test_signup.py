import requests
import json

# Signup data
signup_data = {
    "name": "test",
    "email": "test124@gmail.com",  # Changed email
    "password": "123456",
    "confirm_password": "123456"
}

# Make the request
response = requests.post(
    "http://127.0.0.1:8000/api/core/user_signup/",
    json=signup_data
)

# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")