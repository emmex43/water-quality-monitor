import requests
import json

BASE_URL = "http://localhost:5000"

def test_auth():
    print("🧪 Testing Authentication System...")
    
    # Test data
    user_data = {
        "name": "Community Water Monitor",
        "email": "water@community.org",
        "address": "123 River Street, Watertown",
        "telephone": "+1234567890",
        "password": "securepassword123",
        "organization": "River Conservation Group",
        "role": "community"
    }
    
    # Test Registration
    print("1. Testing registration...")
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test Login
    print("\n2. Testing login...")
    login_data = {
        "email": "water@community.org",
        "password": "securepassword123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test Auth Check
    print("\n3. Testing auth check...")
    response = requests.get(f"{BASE_URL}/api/auth/check")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")

if __name__ == "__main__":
    test_auth()