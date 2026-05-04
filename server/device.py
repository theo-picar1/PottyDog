from flask import Blueprint, jsonify, request

from db import get_db_connection

device_bp = Blueprint("device", __name__)

# Get devices logic
@device_bp.route('/devices', methods=["GET"])
def devices():
  conn = None
  cursor = None
  try:
    user_id = request.args.get('user_id', type=int)
    if user_id is None:
      return jsonify({
        "message": "user_id is required"
      }), 400
      
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
      'SELECT * FROM devices where user_id=%s',
      (user_id,)
    )
    devices = cursor.fetchall()
    return jsonify({
      "devices": devices,
      "message": "Devices successfully fetched"
    }), 200
    
  except Exception as e:
    print(e)
    return jsonify({
      "message": "Server error!"
    }), 500
    
  finally:
    if conn: conn.close()
    if cursor: cursor.close()