import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Secret key for session and CSRF
    SECRET_KEY = os.getenv('SECRET_KEY', 'water-quality-sdg-6-secret-key-2025')

    # Base directory
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # ✅ Database configuration
    # Use DATABASE_URL from Render (MySQL or PostgreSQL)
    # If not provided, fall back to local SQLite for development
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(BASEDIR, '..', 'water_quality.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour (seconds)
