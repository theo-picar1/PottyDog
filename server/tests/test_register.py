import pytest 
from unittest.mock import patch, MagicMock
from app import app

# Automatic setup and teardown of test client
@pytest.fixture 
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test case for going to register page
def test_get_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Create Account" in response.data  # HTML


# Test missing username field
def test_missing_username_register(client):
    data = {
        'username': '',
        'email': 'test@email.com',
        'password': 'Password1!',
    }

    response = client.post('/register', data=data)
    assert response.status_code == 400


# Test missing email field
def test_missing_email_register(client):
    data = {
        'username': 'testuser',
        'email': '',
        'password': 'Password1!',
    }

    response = client.post('/register', data=data)
    assert response.status_code == 400


# Test long username field
def test_long_username_register(client):
    data = {
        'username': 'thisisasuperlongusernamethatnooneshouldbemakingtobeginwithbecausewhywouldyouhaveanamethislong',
        'email': 'test@email.com',
        'password': 'Password1!',
    }

    response = client.post('/register', data=data)
    assert response.status_code == 400


# Test long dog name
def test_long_dog_name_register(client):
    data = {
        'username': 'testuser',
        'email': 'test@email.com',
        'password': 'Password1!',
        'dog_name': 'Imagineyourdogrunsofforwhateverandthisisthenameyouhavetoshoutoutlmao'
    }

    response = client.post('/register', data=data)
    assert response.status_code == 400


# Test missing password field
def test_missing_password_register(client):
    data = {
        'username': 'testuser',
        'email': 'test@email.com',
        'password': ''
    }
    response = client.post('/register', data=data)
    assert response.status_code == 400


# Test invalid email format
def test_invalid_email_register(client):
    data = {
        'username': 'testuser',
        'email': 'thisemailissuperwrong, embarassing!',
        'password': 'Password1!'
    }
    response = client.post('/register', data=data)
    assert response.status_code == 400


# Test weak password 
def test_weak_register_password(client):
    data = {
        'username': 'testuser',
        'email': 'test@email.com',
        'password': 'whoops'
    }
    response = client.post('/register', data=data)
    assert response.status_code == 400


# Test for existing email
@patch('app.get_db_connection')
def test_register_existing_email(mock_db, client):
    # Mock cursor and connection
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = True  # simulate email exists
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    data = {
        'username': 'TestUser',
        'email': 'exists@example.com',
        'password': 'Test123!'
    }

    response = client.post('/register', data=data)
    assert response.status_code == 400