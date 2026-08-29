# Imports
from flask import Blueprint, current_app, render_template, request, session, redirect, url_for, jsonify
import datetime
import jwt
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


# Login logic
@auth_bp.route('/login', methods=['POST'])
def login():
    conn = None
    cursor = None
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({ 
                "message": "All fields are required",
                "status_code": 401
            }), 401

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()
        if not user or not user['password'] == password or user['is_admin'] == True:
            return jsonify({ 
                "message": "Invalid username or password" ,
                "status_code": 401
            }), 401
            
        payload = {
            'id': user['id'],
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)  # expiry
        }
        
        token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm='HS256')
        return jsonify({
            "message": "Success",
            "status_code": 200,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "dog_name": user["dog_name"]
            },
            "token": token
        }), 200
        
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Server error",
            "status_code": 500
        }), 500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Admin login logic
@auth_bp.route('/admin-login', methods=['POST'])
def admin_login():
    conn = None
    cursor = None
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({
                "message": "Please fill in all required fields!"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        admin = cursor.fetchone()
        if not admin or not admin['password'] == password or not bool(admin['is_admin']):
            return jsonify({
                "message": "Incorrect email or password!"
            }), 401
            
        payload = {
            'id': admin['id'],
            'is_admin': True,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)  # expiry
        }
        
        token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm='HS256')

        return jsonify({
            "message": "Success",
            "user": {
                "id": admin["id"],
                "username": admin["username"],
                "email": admin["email"],
                "is_admin": bool(admin["is_admin"])
            },
            "token": token
        }), 200

    except Exception as e:
        print(e)
        return jsonify({
            "message": "Server error!"
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Logging out logic
@auth_bp.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('index'))