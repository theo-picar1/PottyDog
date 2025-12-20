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


# Landing page
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
                    'user_id': session.get('user_id'),
                    'username': session.get('username'),
                    'dog_name': session.get('dog_name')
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


# Dashboard page. Only for logged-in users
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if not 'user_id' in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', dog_name=session.get('dog_name')), 200


# Settings page. Logged-in users only
@app.route('/settings', methods=['GET'])
def settings():
    if not 'user_id' in session:
        return redirect(url_for('login'))

    userData = {
        'user_id': session.get('user_id'),
        'username': session.get('username'),
        'dog_name': session.get('dog_name'),
        'light_mode': session.get('light_mode'),
        'disabled_alerts': session.get('disabled_alerts')
    }

    return render_template('settings.html', userData=userData), 200


# Edit username and/or dog name settings logic
@app.route('/settings/credentials', methods=['PUT', 'POST'])
def update_credentials():
    if request.method == 'POST':
        try:
            conn = None
            cursor = None

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # See if user exists to begin with
            user_id = session.get('user_id')
            cursor.execute(
                "SELECT username, dog_name FROM users where id = %s",
                (user_id,)
            )
            user = cursor.fetchone()
            
            if not user:
                return redirect(url_for('login'))

            updates = []
            values = []
            
            new_username = request.form.get('username')
            new_dog_name = request.form.get('dog_name')

            # Only add fields that have been changed
            if new_username and new_username != user['username'] and len(new_username) < 50:
                updates.append("username = %s")
                values.append(new_username)
                session['username'] = new_username

            if new_dog_name and new_dog_name != user['dog_name'] and len(new_dog_name) < 50:
                updates.append("dog_name = %s")
                values.append(new_dog_name)
                session['dog_name'] = new_dog_name
                
            userData = {
                'username': session.get('username', user['username']),
                'dog_name': session.get('dog_name', user['dog_name']),
                'disabled_alerts': session.get('disabled_alerts'),
                'light_mode': session.get('light_mode')
            }

            if not updates:
                return render_template('settings.html', success="No changes were made!", userData=userData), 200
                
            # Update all fields that have changes to them
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            values.append(user_id)
            cursor.execute(query, tuple(values))
            conn.commit()
            
            return render_template('settings.html', profile_success="Succesfully saved changes!", userData=userData), 200

        except: 
            return render_template('settings.html', error="Error trying to update credentials. Please try again!"), 500
        
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
                
                
# Update preferences for website
@app.route('/settings/preferences', methods=['PUT', 'POST'])
def update_preferences():
    if request.method == 'POST':
        try:
            conn = None
            cursor = None
            
            conn = get_db_connection()
            cursor = conn.cursor()    
            
            # See if user exists to begin with
            user_id = session.get('user_id')
            cursor.execute(
                "SELECT id FROM users where id = %s",
                (user_id,)
            )
            
            user = cursor.fetchone()
            if not user:
                return redirect(url_for('login'))
            
            cursor.execute(
                "SELECT * FROM settings where user_id = %s",
                (user_id,)
            )
            
            preferences = cursor.fetchone()
            if not preferences:
                return render_template('settings.html', error="Error fetching preferences. Please try again!"), 404
            
            # If checkbox was checked, it will not be None 
            disabled_alerts = request.form.get('disabled_alerts') is not None
            light_mode = request.form.get('light_mode') is not None
            
            cursor.execute(
                """
                UPDATE settings 
                SET disabled_alerts = %s, light_mode = %s
                WHERE user_id = %s
                """,
                (disabled_alerts, light_mode, user_id)
            )
            
            conn.commit()
            
            # Update new preferences, if any
            session['disabled_alerts'] = disabled_alerts
            session['light_mode'] = light_mode
            
            userData = {
                'username': session.get('username'),
                'dog_name': session.get('dog_name'),
                'disabled_alerts': session.get('disabled_alerts'),
                'light_mode': session.get('light_mode')
            }
            
            return render_template('settings.html', preferences_success="Successfully saved preferences!", userData=userData)
            
        except:
            return render_template('settings.html', error="Error saving preferences. Please try again!"), 500
            
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()


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

            # Check if that user exists or has incorrect password
            user = cursor.fetchone()
            if not user or not bcrypt.check_password_hash(user['password'], password):
                return render_template('login.html', error="Invalid email or password."), 401
            
            cursor.execute(
                "SELECT light_mode, disabled_alerts FROM settings WHERE user_id = %s",
                (user['id'],)
            )
            
            # Check if settings for them exist
            userSettings = cursor.fetchone()
            if not userSettings:
                return render_template('login.html', error="Could not get all info. Please try again!"), 404
            
            # Store user id in session when successfull
            session.permanent = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['dog_name'] = user['dog_name']
            session['light_mode'] = userSettings['light_mode']
            session['disabled_alerts'] = userSettings['disabled_alerts']
            
            return redirect(url_for('dashboard'))
        
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

            # Create a new row in settings table with user
            user_id = cursor.lastrowid
            cursor.execute(
                """
                INSERT INTO settings (user_id)
                VALUES (%s)
                """,
                (user_id,)
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
        return redirect(url_for('login'))
            
    return render_template('register.html'), 200


# Logging out logic
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)