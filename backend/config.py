import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # FastAPI
    APP_NAME = "Soru Olusturucu API"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "PDF'den sorular algilayan ve olusturan uygulama"
    DEBUG = os.getenv("DEBUG", "False") == "True"
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./soru_olusturucu.db")
    
    # Directories
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_DIR = os.path.join(BASE_DIR, os.getenv("UPLOAD_DIR", "uploads"))
    OUTPUT_DIR = os.path.join(BASE_DIR, os.getenv("OUTPUT_DIR", "outputs"))
    DATA_DIR = os.path.join(BASE_DIR, os.getenv("DATA_DIR", "data"))
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # File limits
    MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
    
    # OCR Settings
    OCR_LANGUAGE = "tr"  # Turkish
    
    @staticmethod
    def ensure_directories():
        """Ensure all required directories exist"""
        for directory in [Config.UPLOAD_DIR, Config.OUTPUT_DIR, Config.DATA_DIR]:
            os.makedirs(directory, exist_ok=True)


# Initialize directories
Config.ensure_directories()
