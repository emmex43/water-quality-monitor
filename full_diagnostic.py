#!/usr/bin/env python3
"""
Full diagnostic of the analytics and role system
"""

from app import create_app
import os

def full_diagnostic():
    print("🔍 FULL SYSTEM DIAGNOSTIC")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        from app.models.user import User
        from app.models.water_quality import WaterQuality
        from app.database.connection import db
        
        print("📊 DATABASE CHECK:")
        print("-" * 30)
        
        # Check users
        users = User.query.all()
        print(f"👥 Users in database: {len(users)}")
        for user in users:
            print(f"   - {user.name} ({user.email}) - Role: {user.role}")
        
        # Check water quality readings
        readings = WaterQuality.query.all()
        print(f"💧 Water quality readings: {len(readings)}")
        for reading in readings:
            print(f"   - {reading.location_name} - Status: {reading.status} - Public: {reading.is_public}")
        
        print("\n🌐 ROUTES CHECK:")
        print("-" * 30)
        
        analytics_routes = []
        for rule in app.url_map.iter_rules():
            if 'analytics' in rule.rule:
                analytics_routes.append(rule.rule)
        
        print(f"📡 Analytics routes found: {len(analytics_routes)}")
        for route in analytics_routes:
            print(f"   ✅ {route}")
        
        print("\n📁 FILES CHECK:")
        print("-" * 30)
        
        # Check critical files
        critical_files = [
            'app/routes/analytics.py',
            'app/templates/analytics_dashboard.html', 
            'app/static/js/analytics.js',
            'app/middleware/auth.py',
            'app/models/user.py',
            'app/models/water_quality.py'
        ]
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                print(f"   ✅ {file_path} - EXISTS")
            else:
                print(f"   ❌ {file_path} - MISSING")
        
        print("\n🎯 ROLE PERMISSIONS CHECK:")
        print("-" * 30)
        
        for user in users:
            print(f"👤 {user.name} (Role: {user.role}):")
            print(f"   - can_view_all_data(): {user.can_view_all_data()}")
            print(f"   - can_edit_all_data(): {user.can_edit_all_data()}")
            print(f"   - is_admin(): {user.is_admin()}")
        
        print("\n🚀 TESTING ANALYTICS ACCESS:")
        print("-" * 30)
        
        with app.test_client() as client:
            for user in users[:2]:  # Test first 2 users
                print(f"\n🧪 Testing with {user.name} ({user.role}):")
                
                # Simulate login
                with client.session_transaction() as session:
                    session['_user_id'] = str(user.id)
                    session['_fresh'] = True
                
                # Test analytics dashboard
                response = client.get('/analytics/dashboard')
                print(f"   📊 /analytics/dashboard: {response.status_code}")
                
                if response.status_code == 200:
                    print("   ✅ Analytics dashboard accessible!")
                else:
                    print(f"   ❌ Cannot access analytics: {response.status_code}")
                
                # Test API
                response = client.get('/analytics/api/statistics')
                print(f"   📡 /analytics/api/statistics: {response.status_code}")

if __name__ == '__main__':
    full_diagnostic()