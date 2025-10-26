#!/usr/bin/env python3
"""
Diagnostic script to find your database and tables
"""

import os
import sqlite3
import glob

def find_database():
    print("🔍 Searching for database files...")
    
    # Common database file locations and patterns
    search_patterns = [
        'instance/*.db',
        'instance/*.sqlite',
        '*.db',
        '*.sqlite',
        'app/instance/*.db',
        'app/*.db',
        'data/*.db',
        '*.sqlite3'
    ]
    
    found_files = []
    for pattern in search_patterns:
        for file_path in glob.glob(pattern):
            if os.path.isfile(file_path):
                found_files.append(file_path)
                print(f"✅ Found: {file_path}")
    
    if not found_files:
        print("❌ No database files found!")
        return False
    
    print(f"\n📊 Found {len(found_files)} database file(s)")
    
    # Check each database file
    for db_file in found_files:
        print(f"\n--- Checking: {db_file} ---")
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if tables:
                print("📋 Tables found:")
                for table in tables:
                    table_name = table[0]
                    print(f"   - {table_name}")
                    
                    # Show columns for this table
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    if columns:
                        column_names = [col[1] for col in columns]
                        print(f"     Columns: {column_names}")
                    else:
                        print(f"     (No columns)")
            else:
                print("   (No tables found)")
            
            conn.close()
            
        except Exception as e:
            print(f"   ❌ Error reading database: {e}")
    
    return True

if __name__ == '__main__':
    find_database()