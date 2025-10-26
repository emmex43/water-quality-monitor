from app.database.connection import db
from datetime import datetime

class WaterQuality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(255), nullable=False)
    ph_level = db.Column(db.Float)
    turbidity_ntu = db.Column(db.Float)
    dissolved_oxygen = db.Column(db.Float)
    temperature_c = db.Column(db.Float)
    conductivity_us = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Link to user who submitted the reading
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # ✅ ADD THESE NEW FIELDS FOR ANALYTICS:
    total_dissolved_solids = db.Column(db.Float)  # ppm - calculated from conductivity
    status = db.Column(db.String(20), default='good')  # excellent, good, fair, poor
    is_public = db.Column(db.Boolean, default=True)  # Whether reading is publicly visible
    
    def to_dict(self):
        return {
            'id': self.id,
            'location_name': self.location_name,
            'ph_level': self.ph_level,
            'turbidity_ntu': self.turbidity_ntu,
            'dissolved_oxygen': self.dissolved_oxygen,
            'temperature_c': self.temperature_c,
            'conductivity_us': self.conductivity_us,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None,
            'user_id': self.user_id,
            # ✅ ADD NEW FIELDS TO DICT:
            'total_dissolved_solids': self.total_dissolved_solids,
            'status': self.status,
            'is_public': self.is_public,
            'status_color': self.get_status_color()  # For frontend display
        }

    # ✅ ADD THESE NEW METHODS FOR ANALYTICS:
    def calculate_status(self):
        """Calculate water quality status based on parameters"""
        score = 0
        
        # pH scoring (ideal: 6.5-8.5)
        if 6.5 <= self.ph_level <= 8.5:
            score += 2
        elif 6.0 <= self.ph_level <= 9.0:
            score += 1
            
        # Dissolved Oxygen scoring (ideal: >5 mg/L)
        if self.dissolved_oxygen >= 5:
            score += 2
        elif self.dissolved_oxygen >= 3:
            score += 1
            
        # Turbidity scoring (ideal: <5 NTU)
        if self.turbidity_ntu <= 5:
            score += 2
        elif self.turbidity_ntu <= 10:
            score += 1
            
        # Determine status
        if score >= 5:
            return 'excellent'
        elif score >= 3:
            return 'good'
        elif score >= 1:
            return 'fair'
        else:
            return 'poor'

    def get_status_color(self):
        """Get Bootstrap color class for status"""
        colors = {
            'excellent': 'success',
            'good': 'info', 
            'fair': 'warning',
            'poor': 'danger'
        }
        return colors.get(self.status, 'secondary')

    def get_status_display_name(self):
        """Get human-readable status name"""
        names = {
            'excellent': 'Excellent',
            'good': 'Good',
            'fair': 'Fair', 
            'poor': 'Poor'
        }
        return names.get(self.status, 'Unknown')

    def calculate_tds(self):
        """Calculate Total Dissolved Solids from conductivity"""
        # Approximate conversion: TDS (ppm) = Conductivity (μS/cm) × 0.64
        if self.conductivity_us:
            return round(self.conductivity_us * 0.64, 2)
        return None

    def before_save(self):
        """Calculate derived values before saving"""
        # Calculate status
        self.status = self.calculate_status()
        
        # Calculate TDS if not provided
        if not self.total_dissolved_solids and self.conductivity_us:
            self.total_dissolved_solids = self.calculate_tds()

    @staticmethod
    def create_table():
        """This method is no longer needed with SQLAlchemy, but we keep it for compatibility"""
        pass