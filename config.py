import os
from dotenv import load_dotenv

# Load .env file if present (for local development)
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is not set")

    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
    if not MONGO_PASSWORD:
        raise ValueError("MONGO_PASSWORD environment variable is not set")

    MONGO_URI = os.getenv('MONGO_URI')
    if not MONGO_URI:
        raise ValueError("MONGO_URI environment variable is not set")

    # Replace placeholder with the actual password
    MONGO_URI = MONGO_URI.replace('<password>', MONGO_PASSWORD)
    
    DEBUG = True
