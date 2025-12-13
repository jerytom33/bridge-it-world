
import requests
import json
import time

print("Testing Aptitude Endpoint...")

url = "http://localhost:8000/api/aptitude/personalized-questions/"
params = {
    "level": "12th",
    "count": 5
}

try:
    # Wait a bit for server to potentialy start if freshly triggered
    time.sleep(2)
    
    print(f"Sending GET request to {url}...")
    response = requests.get(url, params=params, timeout=60)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    
    try:
        data = response.json()
        print("\nResponse JSON:")
        print(json.dumps(data, indent=2))
        
        if response.status_code == 200:
            print("\n✅ Endpoint verification SUCCESS")
        else:
            print(f"\n❌ Endpoint returned error: {data.get('error', 'Unknown error')}")
            
    except json.JSONDecodeError:
        print("\n❌ Response is not valid JSON:")
        print(response.text[:1000]) # First 1000 chars

except Exception as e:
    print(f"\n❌ Request failed: {str(e)}")
