# Imports
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from pubnub.models.consumer.v3.channel import Channel
from flask_bcrypt import Bcrypt
from datetime import timedelta
from dotenv import load_dotenv
from datetime import datetime
import os

# Files
from db import get_db_connection
from pb import create_pubnub, pubnub_bp
from auth import auth_bp
from routes import routes_bp

# Variables
app = Flask(__name__)
app.bcrypt = Bcrypt(app)
app.pubnub = create_pubnub()

DOTENV_PATH = os.getenv('DOTENV_PATH')
if DOTENV_PATH:
    load_dotenv(DOTENV_PATH)  
else:
    load_dotenv()  

# Registering blueprints
app.register_blueprint(pubnub_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(routes_bp)

# Session cookie setup
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
IS_PROD = os.environ.get("FLASK_ENV") == "production"
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=IS_PROD,      
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(days=3)
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
                return redirect(url_for('auth.login'))
            
        except:
            return render_template('index.html'), 500

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    return render_template('index.html'), 200                   
            

# Admin dashboard page
@app.route('/admin-dashboard', methods=['GET'])
def admin_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.admin_login'))
    
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Double check that user did not just add is_admin manually
        cursor.execute(
            'SELECT is_admin FROM users WHERE id = %s',
            (user_id,)
        )
        user = cursor.fetchone()
        
        if not bool(user['is_admin']):
            return render_template(
                'protected.html', 
                status_code='401',
                error="Access denied!",
                message="You do not have the right permissions to access this page!"
            ), 401

        # Only users that have registered a device already and are not admins        
        cursor.execute("""
            SELECT id, username, can_write, can_read FROM users
            WHERE is_admin = FALSE OR is_admin = 0
        """)
        users = cursor.fetchall()
        
        return render_template('admin-dashboard.html', users=users), 200
        
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


# Dashboard page. Only for logged-in users
@app.route('/dashboard', methods=['GET'])
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    conn = None
    cursor = None
    
    # Get most recent potty log and count for today
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT * FROM potty_logs WHERE user_id = %s ORDER BY logged_at DESC LIMIT 1",
            (user_id,)
        )
        last_potty = cursor.fetchone()
        last_potty_time = last_potty['logged_at'].strftime("%b %d, %Y - %H:%M") if last_potty else None
        
        cursor.execute(
            "SELECT COUNT(*) FROM potty_logs WHERE user_id = %s AND DATE(logged_at) = CURDATE()",
            (user_id,)
        )
        activity_count = cursor.fetchone()['COUNT(*)']
        
        user = {
            'username': session.get('username'),
            'dog_name': session.get('dog_name'),
            'can_read': session.get('can_read'),
            'can_write': session.get('can_write'),
            'activity_count': activity_count,
            'last_potty_time': last_potty_time
        }
        
        return render_template('dashboard.html', userData=user, pubnub_sub_key = os.getenv("SUBSCRIBE_KEY")), 200
    
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
            

# Activity page for potty activity
@app.route('/potty-activity', methods=['GET'])
def potty_activity():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    can_read = session.get('can_read')
    if not can_read:
        return render_template(
            'protected.html', 
            status_code="401",
            error="Unauthorised!",
            message="You do not have read access! Please contact the admin to have permissions changed!"
        ), 401

    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        date_param = request.args.get('date')
        date = datetime.strptime(date_param, "%Y-%m-%d").date() if date_param else None
        
        # Get filtered date or default current date
        if date:
            cursor.execute(
                """
                SELECT logged_at, potty_type, notes FROM potty_logs 
                WHERE user_id = %s AND DATE(logged_at) = %s
                """,
                (user_id, date)
            )
        else:
            cursor.execute(
                """
                SELECT logged_at, potty_type, notes FROM potty_logs 
                WHERE user_id = %s AND DATE(logged_at) = CURDATE()
                """,
                (user_id,)
            )
        logs = cursor.fetchall()
        
        user = {
            'username': session.get('username'),
        }
        
        return render_template('potty-activity.html', logs=logs, userData=user), 200
        
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


# Protected page. Shows up when getting any status erros
@app.route('/protected', methods=['GET'])
def protected():
    return render_template('protected.html')


# Unavailable page. SHows up for features / pages not done
@app.route('/unavailable', methods=['GET'])
def unavailable():
    return render_template('unavailble.html')


# Settings page. Logged-in users only
@app.route('/settings', methods=['GET'])
def settings():
    if not 'user_id' in session:
        return redirect(url_for('auth.login'))

    userData = {
        'user_id': session.get('user_id'),
        'username': session.get('username'),
        'dog_name': session.get('dog_name'),
        'light_mode': session.get('light_mode'),
        'disabled_alerts': session.get('disabled_alerts')
    }

    return render_template('settings.html', userData=userData), 200


if __name__ == "__main__":
    app.run(debug=True)