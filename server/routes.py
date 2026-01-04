# Imports
from flask import Blueprint, current_app, render_template, request, session, redirect, url_for

# Files
from db import get_db_connection

routes_bp = Blueprint("routes", __name__)

# Activity count for the day and most recent activity for dashboard
@routes_bp.route('/dashboard/potty-logs', methods=['POST'])
def create_log():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    user = {
        'username': session.get('username'),
        'dog_name': session.get('dog_name'),
        'can_read': session.get('can_read'),
        'can_write': session.get('can_write')
    }
    
    conn = None 
    cursor = None
    
    # Logging time of potty logic
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        potty_type = request.form.get('potty_type')
        notes = request.form.get('description')
        
        if not potty_type:
            return render_template('dashboard.html', error="Please enter a potty type!", user=user), 400
    
        if not notes:
            notes = 'N/A'
            
        cursor.execute(
            """
            INSERT INTO potty_logs (user_id, potty_type, notes)
            VALUES (%s, %s, %s)
            """,
            (user_id, potty_type, notes)
        )
        conn.commit()
        
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

# Change permissions of users from admin dashboard
@routes_bp.route('/admin-dashboard/permissions', methods=['POST'])
def update_permissions():
    user_id = session.get('user_id')
    if not session.get('is_admin') or not user_id:
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
        
        if not bool(user['is_admin']) or bool(user['is_admin']) is False:
            return render_template(
                'protected.html', 
                status_code='401',
                error="Access denied!",
                message="You do not have the right permissions to access this page!"
            ), 401
        
        # Proceed with updating logic 
        cursor.execute("""
            SELECT id, can_read, can_write FROM users 
            WHERE is_admin = FALSE OR is_admin = 0
        """)
        users = cursor.fetchall()

        count = 0
        for user in users:
            id = user['id']
            can_read = user['can_read']
            can_write = user['can_write']
            
            # Read form data: True if checked, False if not
            read_new = f'read_{id}' in request.form
            write_new = f'write_{id}' in request.form

            # Only update if values changed
            if read_new != can_read or write_new != can_write:
                count += 1
                cursor.execute(
                    "UPDATE users SET can_read = %s, can_write = %s WHERE id = %s",
                    (read_new, write_new, id)
                )
                
                # Send to the user's channel that their token has been updated
                current_app.pubnub.publish() \
                    .channel('Channel-Barcelona') \
                    .message({
                        "type": "update_token", 
                        "message": "Your permissions have been changed",
                        "can_read": read_new,
                        "can_write": write_new
                    }) \
                    .sync()

        conn.commit()
        
        # Updated users
        cursor.execute("""
            SELECT id, can_write, username, can_read FROM users 
            WHERE is_admin = FALSE OR is_admin = 0
        """)
        users = cursor.fetchall()
        
        if count > 1:
            return render_template('admin-dashboard.html', success="Successfully changed permissions of selected users!", users=users), 200
        elif count == 1:
            return render_template('admin-dashboard.html', success="Successfully changed permissions of selected user!", users=users), 200
        
        return render_template('admin-dashboard.html', success="No changes were made!", users=users), 200
            
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
            
            
# Edit username and/or dog name settings logic
@routes_bp.route('/settings/credentials', methods=['PUT', 'POST'])
def update_credentials():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        try:
            conn = None
            cursor = None

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # See if user exists to begin with
            cursor.execute(
                "SELECT username, dog_name FROM users where id = %s",
                (user_id,)
            )
            user = cursor.fetchone()
            
            if not user:
                return redirect(url_for('auth.login'))

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
                return render_template('settings.html', profile_success="No changes were made!", userData=userData), 200
                
            # Update all fields that have changes to them
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            values.append(user_id)
            cursor.execute(query, tuple(values))
            conn.commit()
            
            return render_template('settings.html', profile_success="Succesfully saved changes!", userData=userData), 200

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
                
                
# Update preferences for website
@routes_bp.route('/settings/preferences', methods=['PUT', 'POST'])
def update_preferences():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        try:
            conn = None
            cursor = None
            
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)    
            
            # See if user exists to begin with
            cursor.execute(
                "SELECT id FROM users where id = %s",
                (user_id,)
            )
            
            user = cursor.fetchone()
            if not user:
                return redirect(url_for('auth.login'))
            
            cursor.execute(
                "SELECT * FROM settings where user_id = %s",
                (user_id,)
            )
            
            userData = {
                'username': session.get('username'),
                'dog_name': session.get('dog_name'),
                'disabled_alerts': session.get('disabled_alerts'),
                'light_mode': session.get('light_mode')
            }
            
            preferences = cursor.fetchone()
            if not preferences:
                return render_template('settings.html', error="Error fetching preferences. Please try again!", userData=userData), 404
            
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
            
            return render_template('settings.html', preferences_success="Successfully saved preferences!", userData=userData)
            
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