#!/usr/bin/env python3
"""
SQL-Only Database Migration - Most reliable approach
"""

import sqlite3
import os

def sql_migration():
    print("🚀 Starting SQL-only migration...")
    
    # Adjust this path to your actual database file
    db_path = 'instance/water_quality.db'  # Common Flask SQLite location
    if not os.path.exists(db_path):
        db_path = 'water_quality.db'  # Try root directory
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}")
        print("💡 Please check your database file location")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📊 Checking current database structure...")
        
        # Check User table columns
        cursor.execute("PRAGMA table_info(user)")
        user_columns = [col[1] for col in cursor.fetchall()]
        print(f"   - User table columns: {user_columns}")
        
        # Add role column if needed
        if 'role' not in user_columns:
            print("   ➕ Adding 'role' column to user table...")
            cursor.execute('ALTER TABLE user ADD COLUMN role VARCHAR(50) DEFAULT "community"')
            print("   ✅ Added 'role' column")
        else:
            print("   ✅ 'role' column already exists")
        
        # Check WaterQuality table columns
        cursor.execute("PRAGMA table_info(water_quality)")
        water_columns = [col[1] for col in cursor.fetchall()]
        print(f"   - WaterQuality table columns: {water_columns}")
        
        # Add new columns if needed
        new_columns = [
            ('total_dissolved_solids', 'FLOAT'),
            ('status', 'VARCHAR(20) DEFAULT "good"'),
            ('is_public', 'BOOLEAN DEFAULT 1')
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in water_columns:
                print(f"   ➕ Adding '{column_name}' column to water_quality table...")
                cursor.execute(f'ALTER TABLE water_quality ADD COLUMN {column_name} {column_type}')
                print(f"   ✅ Added '{column_name}' column")
            else:
                print(f"   ✅ '{column_name}' column already exists")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("🎉 Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return False

if __name__ == '__main__':
    if sql_migration():
        print("\n✅ Migration completed! You can now run your application.")
    else:
        print("\n❌ Migration failed. Please check the error above.")