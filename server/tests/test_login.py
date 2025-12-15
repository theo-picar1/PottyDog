import pytest 
from unittest.mock import patch, MagicMock
from app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Automatic setup and teardown of test client
@pytest.fixture 
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test going to login page only
def test_get_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login to PottyDog" in response.data


# Test missing email field
def test_missing_email_login(client):
    data = {
        'email': '',
        'password': 'Password1!'
    }

    response = client.post('/login', data=data)
    assert response.status_code == 400
    assert b"Please fill in all required fields!" in response.data


# Test missing password field
def test_missing_password_login(client):
    data = {
        'email': 'test@example.com',
        'password': ''
    }

    response = client.post('/login', data=data)
    assert response.status_code == 400
    assert b"Please fill in all required fields!" in response.data


# Test invalid email credential
@patch('app.get_db_connection')
def test_invalid_email_login(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Simulate no user found

    data = {
        'email': 'nouser@email.com',
        'password': 'Password1!'
    }

    response = client.post('/login', data=data)
    assert response.status_code == 404
    assert b"No existing user found." in response.data


# Test invalid password credential
@patch('app.get_db_connection')
def test_invalid_login_password(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'email': 'test@example.com',
        'password': bcrypt.generate_password_hash('CorrectPassword1!').decode('utf-8')
    } # Example user

    data = {
        'email': 'test@example.com',
        'password': 'WrongPassword1!'
    }

    response = client.post('/login', data=data)
    assert response.status_code == 401
    assert b"Invalid email or password." in response.data