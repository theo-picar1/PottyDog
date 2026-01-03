import sys
import logging

# Add project path
sys.path.insert(0, "/var/www/PottyDog/server")

from app import app as application

# Optional: enable logging to Apache error log
logging.basicConfig(stream=sys.stderr)