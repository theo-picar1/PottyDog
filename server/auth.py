# Imports
from flask import Blueprint, current_app, render_template, request, session, redirect, url_for
import re

# Files
from db import get_db_connection

auth_bp = Blueprint("auth", __name__)

# Registration page and logic
@auth_bp.route('/register', methods=['GET', 'POST'])
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
            
            hashed_password = current_app.bcrypt.generate_password_hash(password).decode('utf-8')

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

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

        except Exception as e:
            print(e) 
            return render_template(
                'protected.html', 
                status_code="500",
                error="Server error!",
                message="Something went wrong. Please contact the admin if issues persist."
            ), 500

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        # Everything passed
        return redirect(url_for('auth.login'))
            
    return render_template('register.html'), 200


# Login page and logic
@auth_bp.route('/login', methods=['GET', 'POST'])
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

            # Check if that user exists or has incorrect password
            cursor.execute(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()
            if not user or not current_app.bcrypt.check_password_hash(user['password'], password):
                return render_template('login.html', error="Invalid email or password."), 401
            
            # Check if settings for them exist
            cursor.execute(
                "SELECT light_mode, disabled_alerts FROM settings WHERE user_id = %s",
                (user['id'],)
            )
            user_settings = cursor.fetchone()
            if not user_settings:
                return render_template('login.html', error="Could not get all info. Please try again!"), 404
            
            # Store necessary user details in session when successful
            session.permanent = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['dog_name'] = user['dog_name']
            session['light_mode'] = user_settings['light_mode']
            session['disabled_alerts'] = user_settings['disabled_alerts']
            session['can_read'] = bool(user['can_read'])
            session['can_write'] = bool(user['can_write'])
            
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            print(e) 
            return render_template(
                'protected.html', 
                status_code="500",
                error="Server error!",
                message="Something went wrong. Please contact the admin if issues persist."
            ), 500
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('login.html'), 200


# Admin login page and logic
@auth_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin-login.html'), 200
    
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template('admin-login.html', error="Please fill in all required fields!"), 400
        
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )
        admin = cursor.fetchone()
        if not admin or not current_app.bcrypt.check_password_hash(admin['password'], password):
            return render_template('admin-login.html', error="Incorrect email or password!"), 401
        
        if not bool(admin['is_admin']):
            return render_template('admin-login.html', error="You are not authorised to use this page!"), 401
        
        # Store necessary user details in session when successful
        session.permanent = True
        session['is_admin'] = True
        session['user_id'] = admin['id']
        
        return redirect(url_for('admin_dashboard'))
            
    except Exception as e:
        print(e)
        return render_template(
            'protected.html', 
            status_code="500",
            error="Server error!",
            message="Something went wrong. Please contact the admin if issues persist."
        ), 500
    
    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()


# Logging out logic
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))