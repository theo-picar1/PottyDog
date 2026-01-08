import sys
import os 
from dotenv import load_dotenv

load_dotenv("/var/www/PottyDog/.env")

# Server folder path
sys.path.insert(0, "/var/www/PottyDog/server")

from app import app as application