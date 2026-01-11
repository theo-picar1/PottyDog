# Imports
from flask import current_app, Blueprint, session, jsonify
from pubnub.models.consumer.v3.channel import Channel
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from dotenv import load_dotenv
import os

# Files
from db import get_db_connection

pubnub_bp = Blueprint("pubnub", __name__)

load_dotenv()

# PubNub setup
def create_pubnub():
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = os.getenv("SUBSCRIBE_KEY")
    pnconfig.publish_key = os.getenv("PUBLISH_KEY")
    pnconfig.secret_key = os.getenv("PUBNUB_SECRET_KEY")
    pnconfig.uuid = "server"
    return PubNub(pnconfig)


# Generate PubNub token for access manager
def generate_token(user_id, read, write, pubnub, ttl=1440):  # ttl in minutes
    try:
        channel = Channel.id("Channel-Barcelona")
        if read:
            channel.read()
        if write:
            channel.write()

        envelope = pubnub.grant_token() \
            .ttl(ttl) \
            .authorized_uuid(f'pottydog-website') \
            .channels([channel]) \
            .sync()

        return envelope.result.token

    except Exception as e:
        print(f"Error generating token: {e}")
        return None


# Give token on login
@pubnub_bp.route('/get_pubnub_token', methods=['POST'])
def get_pubnub_token():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({
            'token': None, 
            'message': "Unauthorized"
        }), 401
    
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if they actually have a device registered to them
        cursor.execute(
            "SELECT id, username, can_read, can_write FROM users WHERE id = %s",
            (user_id,)
        )
        user = cursor.fetchone()
        if not user:
            return jsonify({
                'token': None,
                'message': "Could not generate token! Please try again."
            }), 404
            
        # Get PubNub instance from app.py
        pubnub = current_app.pubnub
        
        # Create the token for the user
        token = generate_token(user_id, bool(user['can_read']), bool(user['can_write']), pubnub)
        if not token:
            return jsonify({
            'token': None, 
            'message': "Could not generate token. Please try again."
        }), 401
            
        return jsonify({
            'token': token,
            'user_id': user_id,
            'username': user['username'],
            'can_read': user['can_read']
        })
    
    except:
        return jsonify({
            'token': None, 
            'message': "Could not generate token. Please try again."
        }), 500
    
    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()