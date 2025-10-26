#!/usr/bin/env python3
"""
Simple Database Migration for Water Quality Monitor
Safe approach that works with your existing Flask app structure
"""

import os
import sys
from flask import Flask

def simple_migration():
    print("🚀 Starting simple database migration...")
    
    # Create a minimal Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///water_quality.db'  # Adjust for your database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize ONLY what we need for migration
    from app.database.connection import db
    db.init_app(app)
    
    with app.app_context():
        try:
            # Get database engine and inspector
            engine = db.engine
            inspector = db.inspect(engine)
            
            print("📊 Checking current database structure...")
            
            # Check and migrate User table
            if engine.has_table('user'):
                user_columns = [col['name'] for col in inspector.get_columns('user')]
                print(f"   - User table columns: {user_columns}")
                
                # Add role column if it doesn't exist
                if 'role' not in user_columns:
                    print("   ➕ Adding 'role' column to user table...")
                    with engine.connect() as conn:
                        conn.execute('ALTER TABLE user ADD COLUMN role VARCHAR(50) DEFAULT "community"')
                    print("   ✅ Added 'role' column")
                else:
                    print("   ✅ 'role' column already exists")
            
            # Check and migrate WaterQuality table  
            if engine.has_table('water_quality'):
                water_columns = [col['name'] for col in inspector.get_columns('water_quality')]
                print(f"   - WaterQuality table columns: {water_columns}")
                
                # Define new columns to add
                new_columns = [
                    ('total_dissolved_solids', 'FLOAT'),
                    ('status', 'VARCHAR(20) DEFAULT "good"'),
                    ('is_public', 'BOOLEAN DEFAULT TRUE')
                ]
                
                for column_name, column_type in new_columns:
                    if column_name not in water_columns:
                        print(f"   ➕ Adding '{column_name}' column to water_quality table...")
                        with engine.connect() as conn:
                            conn.execute(f'ALTER TABLE water_quality ADD COLUMN {column_name} {column_type}')
                        print(f"   ✅ Added '{column_name}' column")
                    else:
                        print(f"   ✅ '{column_name}' column already exists")
            
            print("🎉 Database migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    if simple_migration():
        print("\n✅ Migration completed! You can now run your application.")
        print("\n📋 Next steps:")
        print("   1. Run your Flask app: python run.py")
        print("   2. Test the analytics dashboard: /analytics")
        print("   3. Register a new user with role selection")
    else:
        print("\n❌ Migration failed. Please check the error above.")
        sys.exit(1)