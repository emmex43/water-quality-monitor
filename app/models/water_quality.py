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
            'user_id': self.user_id
        }

    @staticmethod
    def create_table():
        """This method is no longer needed with SQLAlchemy, but we keep it for compatibility"""
        pass