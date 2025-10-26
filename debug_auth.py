#!/usr/bin/env python3
"""
Debug authentication issues
"""

from app import create_app
from app.models.user import User

def debug_auth():
    print("🔐 Debugging Authentication...")
    
    app = create_app()
    
    with app.app_context():
        # Check users and their authentication status
        users = User.query.all()
        print(f"👥 Found {len(users)} users:")
        
        for user in users:
            print(f"   - {user.name} ({user.email}) - Role: {user.role}")
        
        # Test authentication with a specific user
        test_user = users[0] if users else None
        
        if test_user:
            print(f"\n🧪 Testing authentication for {test_user.name}...")
            
            with app.test_client() as client:
                # Simulate login
                with client.session_transaction() as session:
                    session['_user_id'] = str(test_user.id)
                    session['_fresh'] = True
                
                # Test analytics access
                response = client.get('/analytics/dashboard')
                print(f"   📊 /analytics/dashboard: {response.status_code}")
                
                # Check if we got analytics or login page
                if b'Analytics Dashboard' in response.data:
                    print("   ✅ Got analytics content!")
                elif b'Login' in response.data:
                    print("   ❌ Got login page (authentication failed)")
                
                # Test API
                response = client.get('/analytics/api/statistics')
                print(f"   📡 /analytics/api/statistics: {response.status_code}")
                
                # Check if it's JSON or HTML
                content_type = response.content_type
                print(f"   📄 Content-Type: {content_type}")

if __name__ == '__main__':
    debug_auth()