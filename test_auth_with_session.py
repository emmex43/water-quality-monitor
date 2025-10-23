import requests
import json

BASE_URL = "http://localhost:5000"

def test_with_session():
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("🧪 Testing Authentication with Session Management...")
    
    # Test data
    user_data = {
        "name": "Session Test User",
        "email": "session@water.org", 
        "address": "456 Session Street",
        "telephone": "+1234567891",
        "password": "sessionpass123",
        "organization": "Session Test Org",
        "role": "researcher"
    }
    
    # Test Registration
    print("1. Testing registration...")
    response = session.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test Login
    print("\n2. Testing login...")
    login_data = {
        "email": "session@water.org",
        "password": "sessionpass123"
    }
    response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test Auth Check (should now work with session)
    print("\n3. Testing auth check with session...")
    response = session.get(f"{BASE_URL}/api/auth/check")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test Protected Water Endpoints
    print("\n4. Testing protected water endpoints...")
    
    # Add a water reading
    water_data = {
        "location_name": "Session Test River",
        "ph_level": 7.1,
        "turbidity_ntu": 1.8,
        "dissolved_oxygen": 8.2,
        "temperature_c": 21.5,
        "conductivity_us": 320.0
    }
    response = session.post(f"{BASE_URL}/api/water/reading", json=water_data)
    print(f"   Add reading - Status: {response.status_code}")
    print(f"   Add reading - Response: {response.json()}")
    
    # Get user's water readings
    response = session.get(f"{BASE_URL}/api/water/readings")
    print(f"   Get readings - Status: {response.status_code}")
    response_data = response.json()
    print(f"   Get readings - Count: {response_data.get('count', 0)}")
    
    # Test Logout
    print("\n5. Testing logout...")
    response = session.post(f"{BASE_URL}/api/auth/logout")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Verify logout worked
    print("\n6. Verifying logout...")
    response = session.get(f"{BASE_URL}/api/auth/check")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")

if __name__ == "__main__":
    test_with_session()