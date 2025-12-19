from unittest.mock import MagicMock, patch
from flask_bcrypt import Bcrypt
from app import app 
import pytest

bcrypt = Bcrypt(app)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test to see if un-logged user tries to save changes
def test_save_changes_unlogged(client):
    client.post('/logout')
    response = client.post('/settings/credentials', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login to PottyDog' in response.data
    

# Test to see if no changes were made when saving
@patch('app.get_db_connection')
def test_save_changes_no_changes(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'email': 'test@example.com',
        'password': bcrypt.generate_password_hash('CorrectPassword1!').decode('utf-8'),
        'username': 'DaDude',
        'dog_name': 'eaterOfWorlds'
    }

    data = {
        'email': 'test@example.com',
        'password': 'CorrectPassword1!'
    }

    # Login first
    client.post('/login', data=data)
    
    form = {
        'username': 'DaDude',
        'dog_name': 'eaterOfWorlds'
    }
    
    # Then do setting changes
    response = client.post('/settings/credentials', data=form)
    
    assert response.status_code == 200
    assert b'No changes were made!' in response.data
    assert b'DaDude' in response.data
    assert b'eaterOfWorlds' in response.data
    

# Test for invalid username (too long)
@patch('app.get_db_connection')
def test_save_changes_invalid_username(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'email': 'test@example.com',
        'password': bcrypt.generate_password_hash('CorrectPassword1!').decode('utf-8'),
        'username': 'DaDude',
        'dog_name': 'eaterOfWorlds'
    }

    data = {
        'email': 'test@example.com',
        'password': 'CorrectPassword1!'
    }

    # Login first
    client.post('/login', data=data)
    
    form = {
        'username': 'thisusernameiswaytoolonganditisunreasonabletoevenhavethisasausernameonsomeoneswebsitedobetterandgetashorterusername',
        'dog_name': 'eaterOfWorlds'
    }
    
    # No changes should be made
    response = client.post('/settings/credentials', data=form)
    
    assert response.status_code == 200
    assert b'No changes were made!' in response.data
    assert b'DaDude' in response.data
    assert b'eaterOfWorlds' in response.data
    

# Test for invalid dog_name (too long)
@patch('app.get_db_connection')
def test_save_changes_invalid_dog_name(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'email': 'test@example.com',
        'password': bcrypt.generate_password_hash('CorrectPassword1!').decode('utf-8'),
        'username': 'DaDude',
        'dog_name': 'eaterOfWorlds'
    }

    data = {
        'email': 'test@example.com',
        'password': 'CorrectPassword1!'
    }

    # Login first
    client.post('/login', data=data)
    
    form = {
        'username': 'DaDude',
        'dog_name': 'thisusernameiswaytoolonganditisunreasonabletoevenhavethisasausernameonsomeoneswebsitedobetterandgetashorterusername'
    }
    
    # No changes should be made
    response = client.post('/settings/credentials', data=form)
    
    assert response.status_code == 200
    assert b'No changes were made!' in response.data
    assert b'DaDude' in response.data
    assert b'eaterOfWorlds' in response.data
    

# Test to see if changes to both fields are saved
@patch('app.get_db_connection')
def test_save_changes_successful(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'email': 'test@example.com',
        'password': bcrypt.generate_password_hash('CorrectPassword1!').decode('utf-8'),
        'username': 'DaDude',
        'dog_name': 'eaterOfWorlds'
    }

    data = {
        'email': 'test@example.com',
        'password': 'CorrectPassword1!'
    }

    # Login first
    client.post('/login', data=data)
    
    form = {
        'username': 'Batman',
        'dog_name': 'Ace'
    }
    
    # No changes should be made
    response = client.post('/settings/credentials', data=form)
    
    assert response.status_code == 200
    assert b'Batman' in response.data
    assert b'Ace' in response.data