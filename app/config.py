import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'water-quality-sdg-6-secret-key-2025')
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, '..', 'water_quality.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600
