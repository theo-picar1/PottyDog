# Imports
from dotenv import load_dotenv
import mysql.connector
import os

DOTENV_PATH = os.getenv('DOTENV_PATH')

if DOTENV_PATH:
    load_dotenv(DOTENV_PATH)  
else:
    load_dotenv()  
    
# DB credentials
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

# DB helper function
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        use_pure=True # Does not work without it.
    )