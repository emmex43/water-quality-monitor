#!/usr/bin/env python3
"""
Update existing users with proper roles
"""

import sqlite3

def update_user_roles():
    print("🔄 Updating existing user roles...")
    
    db_path = 'water_quality.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current user roles
        cursor.execute("SELECT id, name, email, role FROM user")
        users = cursor.fetchall()
        
        print(f"📋 Found {len(users)} users:")
        for user_id, name, email, role in users:
            print(f"   - {name} ({email}): role = {role}")
        
        # Update NULL or empty roles to 'community'
        cursor.execute("UPDATE user SET role = 'community' WHERE role IS NULL OR role = ''")
        
        # Optionally, upgrade a specific user to researcher for testing
        if users:
            # Upgrade the first user to researcher
            first_user_id = users[0][0]
            cursor.execute("UPDATE user SET role = 'researcher' WHERE id = ?", (first_user_id,))
            print(f"   ⬆️  Upgraded {users[0][1]} to 'researcher' role")
        
        conn.commit()
        
        # Verify changes
        cursor.execute("SELECT name, email, role FROM user")
        updated_users = cursor.fetchall()
        
        print("\n✅ Updated user roles:")
        for name, email, role in updated_users:
            print(f"   - {name}: {role}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Update failed: {str(e)}")
        return False

if __name__ == '__main__':
    if update_user_roles():
        print("\n🎉 User roles updated! You can now test all features with your existing account.")
    else:
        print("\n❌ Update failed.")