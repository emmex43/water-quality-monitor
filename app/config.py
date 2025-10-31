import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ✅ SECURITY CRITICAL: Use ONLY environment variable, no hardcoded fallback in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # ✅ DATABASE: Use Render's PostgreSQL or environment variable
    # Handles both PostgreSQL (Render) and SQLite (development)
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///water_quality.db')
    
    # Fix for PostgreSQL URL format (Render uses postgres://, SQLAlchemy needs postgresql://)
    if database_url.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = database_url.replace('postgres://', 'postgresql://', 1)
    else:
        SQLALCHEMY_DATABASE_URI = database_url
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600