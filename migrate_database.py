#!/usr/bin/env python3
"""
Database Migration Script for Water Quality Monitor
Adds new fields for role-based access and analytics
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database.connection import db, init_database
from app import create_app
from app.models.user import User
from app.models.water_quality import WaterQuality

def migrate_database():
    """Migrate database to add new fields"""
    print("🚀 Starting database migration...")
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        try:
            # Initialize database connection
            init_database(app)
            
            print("📊 Current database state:")
            print(f"   - User table exists: {db.engine.has_table('user')}")
            print(f"   - WaterQuality table exists: {db.engine.has_table('water_quality')}")
            
            # Get existing table information
            inspector = db.inspect(db.engine)
            
            if db.engine.has_table('user'):
                user_columns = [col['name'] for col in inspector.get_columns('user')]
                print(f"   - User table columns: {user_columns}")
                
                # Check if new columns exist, if not add them
                if 'role' not in user_columns:
                    print("   ➕ Adding 'role' column to user table...")
                    db.engine.execute('ALTER TABLE user ADD COLUMN role VARCHAR(50) DEFAULT "community"')
                    print("   ✅ Added 'role' column")
            
            if db.engine.has_table('water_quality'):
                water_columns = [col['name'] for col in inspector.get_columns('water_quality')]
                print(f"   - WaterQuality table columns: {water_columns}")
                
                # Add new columns if they don't exist
                new_columns = {
                    'total_dissolved_solids': 'FLOAT',
                    'status': 'VARCHAR(20) DEFAULT "good"',
                    'is_public': 'BOOLEAN DEFAULT TRUE'
                }
                
                for column_name, column_type in new_columns.items():
                    if column_name not in water_columns:
                        print(f"   ➕ Adding '{column_name}' column to water_quality table...")
                        db.engine.execute(f'ALTER TABLE water_quality ADD COLUMN {column_name} {column_type}')
                        print(f"   ✅ Added '{column_name}' column")
            
            print("🎉 Database migration completed successfully!")
            print("\n📋 Migration Summary:")
            print("   - User.role: Added for role-based access control")
            print("   - WaterQuality.total_dissolved_solids: Added for TDS tracking")
            print("   - WaterQuality.status: Added for automated quality rating")
            print("   - WaterQuality.is_public: Added for data privacy control")
            
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            return False
    
    return True

if __name__ == '__main__':
    if migrate_database():
        print("\n✅ Migration completed! You can now run your application.")
    else:
        print("\n❌ Migration failed. Please check the error above.")
        sys.exit(1)