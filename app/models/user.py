from app.database.connection import db
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime

bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    organization = db.Column(db.String(100))
    role = db.Column(db.String(50), default='community')  # ✅ Already have role field!
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with water quality readings
    water_readings = db.relationship('WaterQuality', backref='author', lazy=True)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    # ✅ ADD THESE NEW ROLE-BASED METHODS:
    def has_role(self, role_name):
        """Check if user has specific role"""
        return self.role == role_name
    
    def can_view_all_data(self):
        """Check if user can view all data (not just their own)"""
        return self.role in ['researcher', 'government', 'admin']
    
    def can_edit_all_data(self):
        """Check if user can edit all data"""
        return self.role in ['government', 'admin']
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def get_role_display_name(self):
        """Get human-readable role name"""
        role_names = {
            'community': 'Community Member',
            'researcher': 'Researcher', 
            'government': 'Government Official',
            'admin': 'System Administrator'
        }
        return role_names.get(self.role, self.role.title())
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'organization': self.organization,
            'role': self.role,
            'role_display': self.get_role_display_name()  # ✅ Added role display
        }