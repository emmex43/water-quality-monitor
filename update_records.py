#!/usr/bin/env python3
"""
Update existing water quality records with calculated status and TDS
"""

import sqlite3

def update_existing_records():
    print("🔄 Updating existing water quality records...")
    
    db_path = 'water_quality.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all existing records
        cursor.execute("SELECT id, ph_level, dissolved_oxygen, turbidity_ntu, conductivity_us FROM water_quality")
        records = cursor.fetchall()
        
        print(f"📝 Found {len(records)} records to update...")
        
        updated_count = 0
        
        for record_id, ph, do, turbidity, conductivity in records:
            # Calculate water quality status
            score = 0
            
            # pH scoring (ideal: 6.5-8.5)
            if ph and 6.5 <= ph <= 8.5:
                score += 2
            elif ph and 6.0 <= ph <= 9.0:
                score += 1
                
            # Dissolved Oxygen scoring (ideal: >5 mg/L)
            if do and do >= 5:
                score += 2
            elif do and do >= 3:
                score += 1
                
            # Turbidity scoring (ideal: <5 NTU)
            if turbidity and turbidity <= 5:
                score += 2
            elif turbidity and turbidity <= 10:
                score += 1
            
            # Determine status
            if score >= 5:
                status = 'excellent'
            elif score >= 3:
                status = 'good'
            elif score >= 1:
                status = 'fair'
            else:
                status = 'poor'
            
            # Calculate TDS from conductivity
            tds = conductivity * 0.64 if conductivity else None
            
            # Update the record
            cursor.execute('''
                UPDATE water_quality 
                SET status = ?, total_dissolved_solids = ?, is_public = 1
                WHERE id = ?
            ''', (status, tds, record_id))
            
            updated_count += 1
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print(f"✅ Updated {updated_count} water quality records")
        print("   - Added quality status ratings")
        print("   - Calculated TDS values from conductivity")
        print("   - Set all records as public by default")
        
        return True
        
    except Exception as e:
        print(f"❌ Update failed: {str(e)}")
        return False

if __name__ == '__main__':
    if update_existing_records():
        print("\n🎉 Records updated! Your analytics dashboard should now work perfectly!")
    else:
        print("\n❌ Update failed.")