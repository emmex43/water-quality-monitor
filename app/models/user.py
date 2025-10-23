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
    role = db.Column(db.String(50), default='community')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with water quality readings
    water_readings = db.relationship('WaterQuality', backref='author', lazy=True)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'organization': self.organization,
            'role': self.role
        }