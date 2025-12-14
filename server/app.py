from flask import Flask, render_template, request, redirect
import re
from flask_bcrypt import Bcrypt
import os
import mysql.connector
from dotenv import load_dotenv
import traceback

app = Flask(__name__)
bcrypt = Bcrypt(app)

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


# Main page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Login page and logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


# Registration page and logic
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cursor = None
        conn = None
        
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            dog_name = request.form.get('dog_name') # Not required
            password = request.form.get('password')

            # Case handling for registering
            if not username or not email or not password:
                return render_template('register.html', error="Please fill in all required fields!"), 400
            
            if len(username) > 50:
                return render_template('register.html', error="Username must be 50 characters or fewer."), 400
            
            if dog_name and len(dog_name) > 25:
                return render_template('register.html', error="Dog name must be 25 characters or fewer."), 400
            
            # Standard email format
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                return render_template('register.html', error="Invalid email format."), 400
            
            # At least 8 characters, one uppercase, one lowercase, one digit, one special character
            password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
            if not re.match(password_regex, password):
                return render_template('register.html', error="Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character."), 400
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if email already exists
            cursor.execute(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )
            if cursor.fetchone():
                return render_template('register.html', error="An account with this email already exists."), 400

            # Otherwise, proceed
            cursor.execute(
                """
                INSERT INTO users (username, email, dog_name, password)
                VALUES (%s, %s, %s, %s)
                """,
                (username, email, dog_name, hashed_password)
            )

            conn.commit()

        except:
            return render_template('register.html', error="An error occurred during registration. Please try again."), 500

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        # Everything passed
        return render_template('login.html'), 200
            
    return render_template('register.html'), 200


if __name__ == "__main__":
    app.run(debug=True)