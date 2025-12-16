from flask import Flask, render_template, request, session, redirect, url_for
from flask_bcrypt import Bcrypt
from datetime import timedelta
from dotenv import load_dotenv
import mysql.connector
import re
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

load_dotenv()

# Session cookie setup
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
IS_PROD = os.environ.get("FLASK_ENV") == "production"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=IS_PROD,      
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(days=3)
)

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
    if 'user_id' in session:
        user_id = session['user_id']
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE id = %s",
                (user_id,)
            )

            user = cursor.fetchone()
            
            if user:
                userData = {
                    'username': user['username'],
                    'dog_name': user['dog_name']
                }

                return render_template('index.html', userData=userData), 200
            else:
                # The user no longer exists in db
                session.pop('user_id', None)
                return redirect(url_for('/login'))

        except:
            return render_template('index.html'), 500

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    return render_template('index.html'), 200


# Login page and logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = None
        cursor = None

        try:
            email = request.form.get('email')
            password = request.form.get('password')

            if not email or not password:
                return render_template('login.html', error="Please fill in all required fields!"), 400

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )

            # Check if that user exists
            user = cursor.fetchone()
            if not user:
                return render_template('login.html', user_error="No existing user found."), 404
            
            # Check two passwords with each other
            if not bcrypt.check_password_hash(user['password'], password):
                return render_template('login.html', error="Invalid email or password."), 401
            
            # Store user id in session when successsfull
            session.permanent = True
            session['user_id'] = user['id']

            userData = {
                'username': user['username'],
                'dog_name': user['dog_name']
            }
            
            return render_template('index.html', userData=userData), 200
        
        except:
            return render_template('login.html', error="An error occurred during login. Please try again."), 500
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('login.html'), 200


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
            confirm_password = request.form.get('confirm_password')

            # Case handling for registering
            if not username or not email or not password:
                return render_template('register.html', error="Please fill in all required fields!"), 400
            
            if len(username) > 50:
                return render_template('register.html', long_username_error="Username must be 50 characters or fewer."), 400
            
            if dog_name and len(dog_name) > 25:
                return render_template('register.html', long_dog_name_error="Dog name must be 25 characters or fewer."), 400
            
            # Standard email format
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                return render_template('register.html', email_format_error="Invalid email format."), 400
            
            # At least 8 characters, one uppercase, one lowercase, one digit, one special character
            password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
            if not re.match(password_regex, password):
                return render_template('register.html', weak_password_error="Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character."), 400
            
            if confirm_password and confirm_password != password:
                return render_template('register.html', confirm_password_error="Passwords do not match."), 400
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if email already exists
            cursor.execute(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )
            if cursor.fetchone():
                return render_template('register.html', existing_user_error="An account with this email already exists."), 400

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


# Logging out logic
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)