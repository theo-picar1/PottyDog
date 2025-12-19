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


# Test un-logged user 
def test_get_index_unlogged(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Please register or login to continue." in response.data


# Test logged-in user
@patch('app.get_db_connection')
def test_get_index_logged(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'username': 'TheoPic',
        'dog_name': 'Lala'
    }

    # Set up session directly instead of logging in first
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'TheoPic'
        session['dog_name'] = 'Lala'

    response = client.get('/')

    assert response.status_code == 200
    assert b'You are logged in! You can now head over to the dashboard page!' in response.data


# Test logged out user
def test_get_index_logged_out(client):
    with client.session_transaction() as session:
        session.clear()
        
    response = client.get('/')

    assert b"Please register or login to continue." in response.data


# Test getting settings page unlogged
def test_get_settings_logged_out(client):
    with client.session_transaction() as session:
        session.clear() 
    
    response = client.get('/settings', follow_redirects=True)

    assert b"Login to PottyDog" in response.data


# Test getting settings page logged-in
@patch('app.get_db_connection')
def test_get_settings_logged_in(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'username': 'TheoPic',
        'dog_name': 'Lala'
    }

    with client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'TheoPic'
        session['dog_name'] = 'Lala'
        
    response = client.get('/dashboard')

    assert response.status_code == 200
    assert b'Dog Potty tracker' in response.data


# Test getting dashboard page unlogged
def test_get_dashboard_logged_out(client):
    with client.session_transaction() as session:
        session.clear()
        
    response = client.get('/dashboard', follow_redirects=True)

    assert b"Login to PottyDog" in response.data


# Test getting dashboard page logged-in
@patch('app.get_db_connection')
def test_get_settings_logged_in(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'username': 'TheoPic',
        'dog_name': 'Lala'
    }

    with client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'TheoPic'
        session['dog_name'] = 'Lala'
        
    response = client.get('/settings')

    assert response.status_code == 200
    assert b'TheoPic' in response.data
    assert b'Lala' in response.data