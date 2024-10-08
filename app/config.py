import os  # Import the os module to use getenv
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
# Database configuration
conf = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('')
}

class Config:
    SQLALCHEMY_DATABASE_URI=f"postgresql://{conf['user']}:{conf['password']}@{conf['host']}:5432/postgres"
    JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')
    JWT_SECRET_KEY_EXPIRES= timedelta(hours=24)

