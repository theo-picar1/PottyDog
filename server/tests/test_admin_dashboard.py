from unittest.mock import patch, MagicMock
from flask_bcrypt import Bcrypt
from app import app
import pytest

bcrypt = Bcrypt(app)

# Automatic setup and teardown of test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
        
# Test to see if user tries to go into admin dashboard with expired session
def test_session_missing_user_id(client):
    with client.session_transaction() as session:
        session.clear()
    
    response = client.get('/admin-dashboard', follow_redirects=True)
    
    assert b"Administrator Login" in response.data
        

# Test to see if non admin tries to go into admin dashboard
@patch('app.get_db_connection')
def test_get_dashboard_unauthorised(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'email': 'theopic@email.com',
        'is_admin': False
    }
    
    with client.session_transaction() as session:
        session['user_id'] = 1
    
    response = client.get('/admin-dashboard', follow_redirects=True)
    
    assert response.status_code == 401
    assert b"You do not have the right permissions to access this page!" in response.data
    
    
# Test to see if admin can log in
@patch('app.get_db_connection')
def test_get_dashboard_authorised(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'email': 'theopic@email.com',
        'is_admin': True
    }
    
    with client.session_transaction() as session:
        session['user_id'] = 1
        
    response = client.get('/admin-dashboard')
        
    assert response.status_code == 200
    assert b"Manage PubNub access for your users." in response.data
    

# Test to see if users load in properly if they exist
@patch('app.get_db_connection')
def test_get_dashboard_users_loaded(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'email': 'theopic@email.com',
        'is_admin': True
    }
    mock_cursor.fetchall.return_value = [
        {'id': 2, 'username': 'lalapic', 'can_write': 1, 'can_read': 1},
        {'id': 3, 'username': 'piclala', 'can_write': 0, 'can_read': 1},
    ]
    
    with client.session_transaction() as session:
        session['user_id'] = 1
        
    response = client.get('/admin-dashboard')
        
    assert response.status_code == 200
    assert b"lalapic" in response.data
    assert b"piclala" in response.data
    
    
# Test to see if appropriate message shows up with no users
@patch('app.get_db_connection')
def test_get_dashboard_no_users(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'email': 'theopic@email.com',
        'is_admin': True
    }
    mock_cursor.fetchall.return_value = []
    
    with client.session_transaction() as session:
        session['user_id'] = 1
        
    response = client.get('/admin-dashboard')
        
    assert response.status_code == 200
    assert b"No users available!" in response.data
    

# Test for 500 error
@patch('app.get_db_connection')
def test_admin_dashboard_user_missing(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  
    
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.get('/admin-dashboard')

    assert response.status_code == 500
    assert b"Something went wrong" in response.data