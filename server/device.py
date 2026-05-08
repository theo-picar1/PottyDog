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
  
    
# Get device by id
@device_bp.route('/devices/<int:id>', methods=["GET"])
def device(id):
  conn = None
  cursor = None
  try:
    if not id or id is None:
      return jsonify({
        "message": "Device id must be provided"
      }), 400
      
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
      "SELECT * FROM devices WHERE id = %s",
      (id,)
    )
    
    device = cursor.fetchone()
    if not device or device is None:
      return jsonify({
        "message": "No device has been found with ID {id}"
      }), 404
      
    return jsonify({
      "message": "Successfully retrieved device with ID {id}",
      "device": device
    }), 200
    
  except Exception as e:
    print(e)
    jsonify({
      "message": "Something went wrong. Please try again."
    }), 500
    
  finally:
    if conn: conn.close()
    if cursor: cursor.close()
    
    
# Edit device
@device_bp.route('/devices/<int:id>', methods=["PUT"])
def edit_device(id):
  conn = None
  cursor = None
  try:
    data = request.get_json()
    device_name = data.get('deviceName')
    device_location = data.get('deviceLocation')
    if not device_name or not device_location:
      return jsonify({
        "message": "All fields must have values"
      }), 400
      
    if not id or id is None:
      return jsonify({
        "message": "No device was provided"
      }), 400
      
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
      'SELECT * FROM devices WHERE id = %s',
      (id,)
    )
    
    device = cursor.fetchone()
    if not device or device is None:
      return jsonify({
        "message": "No matching device found"
      }), 404
      
    cursor.execute(
      "UPDATE devices SET device_name = %s, device_location= %s WHERE id = %s",
      (device_name, device_location, id,)
    )
    
    conn.commit()
    return jsonify({
      "message": "Successfully updated device with ID {id}"
    }), 200
    
  except Exception as e:
    print(e)
    return jsonify({
      "message": "Server error!"
    }), 500
    
  finally:
    if conn: conn.close()
    if cursor: cursor.close()