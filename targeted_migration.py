#!/usr/bin/env python3
"""
Targeted Migration - Only adds missing columns to water_quality table
"""

import sqlite3
import os

def targeted_migration():
    print("🚀 Starting targeted database migration...")
    
    # Use the correct database file
    db_path = 'water_quality.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📊 Checking water_quality table structure...")
        
        # Check current water_quality columns
        cursor.execute("PRAGMA table_info(water_quality)")
        water_columns = [col[1] for col in cursor.fetchall()]
        print(f"   - Current columns: {water_columns}")
        
        # Define only the missing columns we need to add
        missing_columns = [
            ('total_dissolved_solids', 'FLOAT'),
            ('status', 'VARCHAR(20) DEFAULT "good"'),
            ('is_public', 'BOOLEAN DEFAULT 1')
        ]
        
        columns_added = 0
        
        for column_name, column_type in missing_columns:
            if column_name not in water_columns:
                print(f"   ➕ Adding '{column_name}' column...")
                cursor.execute(f'ALTER TABLE water_quality ADD COLUMN {column_name} {column_type}')
                print(f"   ✅ Added '{column_name}' column")
                columns_added += 1
            else:
                print(f"   ✅ '{column_name}' column already exists")
        
        # Commit changes
        conn.commit()
        
        # Verify the changes
        cursor.execute("PRAGMA table_info(water_quality)")
        final_columns = [col[1] for col in cursor.fetchall()]
        print(f"   - Final columns: {final_columns}")
        
        conn.close()
        
        if columns_added > 0:
            print(f"🎉 Successfully added {columns_added} new columns!")
        else:
            print("ℹ️  All columns already exist - no changes needed.")
            
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return False

if __name__ == '__main__':
    if targeted_migration():
        print("\n✅ Migration completed successfully!")
        print("\n📋 What was added:")
        print("   - total_dissolved_solids: For TDS tracking")
        print("   - status: For automated water quality rating") 
        print("   - is_public: For data privacy control")
        print("\n🚀 You can now run your Flask app and test the new features!")
    else:
        print("\n❌ Migration failed.")