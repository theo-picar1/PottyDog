import sys
import logging
from dotenv import load_dotenv

# Server folder path
sys.path.insert(0, "/var/www/PottyDog/server")

# Load .env 
project_root = Path("/var/www/PottyDog")
load_dotenv(dotenv_path=project_root / ".env")

from app import app as application