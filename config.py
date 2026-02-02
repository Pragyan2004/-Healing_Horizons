import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'breakup-recovery-2026-secret-key')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///recovery.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Indian localization
    COUNTRY = 'India'
    CURRENCY = 'INR'
    TIMEZONE = 'Asia/Kolkata'
    
    # Feature flags
    ENABLE_JOURNAL = True
    ENABLE_COMMUNITY = True
    ENABLE_PROGRESS_TRACKING = True