#!/usr/bin/env python3
"""
Direct test of analytics features
"""

from app import create_app

def test_analytics():
    print("🔍 Testing Analytics Directly...")
    
    app = create_app()
    
    with app.app_context():
        with app.test_client() as client:
            # Test 1: Check if we can access analytics dashboard
            print("\n1. Testing Analytics Dashboard Access...")
            response = client.get('/analytics/dashboard', follow_redirects=True)
            print(f"   Status Code: {response.status_code}")
            print(f"   Content Length: {len(response.data)} bytes")
            
            if response.status_code == 200:
                print("   ✅ Analytics dashboard accessible!")
                # Check if it contains analytics content
                if b'Analytics Dashboard' in response.data:
                    print("   ✅ Analytics content found!")
                else:
                    print("   ❌ Analytics content NOT found!")
            else:
                print("   ❌ Cannot access analytics dashboard")
            
            # Test 2: Check API endpoints
            print("\n2. Testing Analytics API Endpoints...")
            endpoints = [
                '/analytics/api/statistics',
                '/analytics/api/quality-distribution',
                '/analytics/api/water-quality-trends'
            ]
            
            for endpoint in endpoints:
                response = client.get(endpoint, follow_redirects=True)
                print(f"   {endpoint}: {response.status_code}")
                if response.status_code == 200:
                    print(f"   ✅ Data: {len(response.data)} bytes")
            
            # Test 3: Check if templates exist
            print("\n3. Checking Template Files...")
            try:
                with app.app_context():
                    template = app.jinja_env.get_template('analytics_dashboard.html')
                    print("   ✅ analytics_dashboard.html template loaded")
            except Exception as e:
                print(f"   ❌ Template error: {e}")
            
            # Test 4: Check static files
            print("\n4. Checking Static Files...")
            static_files = [
                '/static/js/analytics.js',
                '/static/css/style.css'
            ]
            
            for static_file in static_files:
                response = client.get(static_file)
                print(f"   {static_file}: {response.status_code}")

if __name__ == '__main__':
    test_analytics()