import requests
import sys

def test_fcm_endpoints():
    base_url = "http://127.0.0.1:8000/api/core"
    
    # 1. Login to get token
    # Note: Login logic might differ based on your specific auth views
    # Assuming standard JWT token obtain pair or custom login
    login_url = f"{base_url}/login/"
    login_data = {
        "email": "rahul@gmail.com",
        "password": "123456"
    }
    
    try:
        print(f"Testing login at {login_url}...")
        response = requests.post(login_url, data=login_data)
        
        if response.status_code != 200:
             print(f"Login failed: {response.text}")
             # Try auth/login/ path if core/login/ fails
             base_url_alt = "http://127.0.0.1:8000/api/auth"
             login_url = f"{base_url_alt}/login/"
             print(f"Retrying login at {login_url}...")
             response = requests.post(login_url, json=login_data)
             
             if response.status_code != 200:
                print(f"Login failed again: {response.text}")
                return

        token = response.json().get('token')
        headers = {'Authorization': f'Bearer {token}'}
        print("Login successful. Token obtained.")

        # 2. Register FCM Token
        register_url = "http://127.0.0.1:8000/api/core/fcm/register/"
        fcm_data = {
            "token": "test_fcm_device_token_12345",
            "device_type": "android"
        }
        print(f"Testing token registration at {register_url}...")
        reg_response = requests.post(register_url, json=fcm_data, headers=headers)
        print(f"Registration Status: {reg_response.status_code}")
        print(f"Registration Response: {reg_response.text}")

        # 3. Send Test Notification
        test_url = "http://127.0.0.1:8000/api/core/fcm/test/"
        print(f"Testing notification send at {test_url}...")
        test_response = requests.post(test_url, headers=headers)
        print(f"Test Notification Status: {test_response.status_code}")
        print(f"Test Notification Response: {test_response.text}")

    except Exception as e:
        print(f"Test failed with error: {e}")

if __name__ == "__main__":
    test_fcm_endpoints()
