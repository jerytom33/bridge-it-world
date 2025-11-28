import requests

# Test the profile API
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0MjYyOTQwLCJpYXQiOjE3NjQyNjI2NDAsImp0aSI6IjY2ZjRjY2IxNDViOTQwM2NiZGE1M2Q1ZDgxOTkzOTA3IiwidXNlcl9pZCI6IjQifQ.aGXsb1ScLHZ5J0NBdYCMpRknj58yHTE0bXCpWl_0dcU"
headers = {"Authorization": f"Bearer {token}"}

# Test GET request
response = requests.get("http://127.0.0.1:8000/api/core/profile-api/", headers=headers)
print(f"GET Status Code: {response.status_code}")
print(f"GET Response: {response.json()}")

# Test POST request with profile data
profile_data = {
    "phone": "1234567890",
    "education_level": "ug",
    "stream": "Computer Science",
    "interests": ["programming", "AI"],
    "career_goals": "Become a software developer"
}

response = requests.post("http://127.0.0.1:8000/api/core/profile-api/", json=profile_data, headers=headers)
print(f"POST Status Code: {response.status_code}")
print(f"POST Response: {response.json()}")