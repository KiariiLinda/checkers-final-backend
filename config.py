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