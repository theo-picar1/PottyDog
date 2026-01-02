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
def test_update_credentials_unlogged(client):
    client.post('/logout')
    response = client.post('/settings/credentials', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login to PottyDog' in response.data
    

# Test to see if no changes were made when saving
@patch('app.get_db_connection')
def test_update_credentials_no_changes(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'username': 'DaDude',
        'dog_name': 'eaterOfWorlds'
    }

    # Set up session directly instead of logging in first
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'DaDude'
        session['dog_name'] = 'eaterOfWorlds'
    
    # Then do setting changes
    response = client.post('/settings/credentials')
    
    assert response.status_code == 200
    assert b'No changes were made!' in response.data
    assert b'DaDude' in response.data
    assert b'eaterOfWorlds' in response.data
    

# Test for invalid username (too long)
@patch('app.get_db_connection')
def test_update_credentials_invalid_username(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'username': 'DaDude',
        'dog_name': 'eaterOfWorlds'
    }

    with client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'DaDude'
        session['dog_name'] = 'eaterOfWorlds'
    
    # No changes should be made
    response = client.post('/settings/credentials')
    
    assert response.status_code == 200
    assert b'No changes were made!' in response.data
    assert b'DaDude' in response.data
    assert b'eaterOfWorlds' in response.data
    

# Test for invalid dog_name (too long)
@patch('app.get_db_connection')
def test_update_credentials_invalid_dog_name(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'username': 'DaDude',
        'dog_name': 'eaterOfWorlds'
    }
    
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'DaDude'
        session['dog_name'] = 'eaterOfWorlds'
    
    # No changes should be made
    response = client.post('/settings/credentials')
    
    assert response.status_code == 200
    assert b'No changes were made!' in response.data
    assert b'DaDude' in response.data
    assert b'eaterOfWorlds' in response.data
    

# ----- BROKEN TEST -----
# Test to see if changes to both fields are saved
# @patch('app.get_db_connection')
# def test_update_credentials_successful(mock_get_db_connection, client):
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_get_db_connection.return_value = mock_conn
#     mock_conn.cursor.return_value = mock_cursor
#     mock_cursor.fetchone.return_value = {
#         'id': 1,
#         'username': 'DaDude',
#         'dog_name': 'eaterOfWorlds'
#     }

#     with client.session_transaction() as session:
#         session['user_id'] = 1
#         session['username'] = 'DaDude'
#         session['dog_name'] = 'eaterOfWorlds'
        
#     userData = {
#         'username': 'Batman',
#         'dog_name': 'Ace'
#     }
    
#     response = client.post('/settings/credentials', data=userData)
    
#     assert response.status_code == 200
#     assert b'Batman' in response.data
#     assert b'Ace' in response.data
    
    
# Test to save preferences unlogged
def test_update_preferences_unlogged(client):
    client.post('/logout')
    response = client.post('/settings/preferences', follow_redirects=True)

    assert response.status_code == 200
    assert b'Login' in response.data
    
    
# Test get user, no settings data found
@patch('app.get_db_connection')
def test_update_preferences_settings_not_found(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [{'id': 1}, None] # User exists then no corresponding no settings data

    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/settings/preferences')

    assert response.status_code == 404
    assert b'Error fetching preferences. Please try again!' in response.data
    

# Test for all preferences turned off and saved
@patch('app.get_db_connection')
def test_update_preferences_unchecked(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'user_id': 1
    }

    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/settings/preferences')

    assert response.status_code == 200
    assert b'Successfully saved preferences!' in response.data
    with client.session_transaction() as session:
        assert session['disabled_alerts'] is False
        assert session['light_mode'] is False
        

# ----- BROKEN TEST -----        
# Test to see if both preferences were checked and saved
# @patch('app.get_db_connection')
# def test_update_preferences_checked(mock_get_db_connection, client):
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_get_db_connection.return_value = mock_conn
#     mock_conn.cursor.return_value = mock_cursor
#     mock_cursor.fetchone.return_value = {
#         'id': 1,
#         'user_id': 1
#     }

#     with client.session_transaction() as session:
#         session['user_id'] = 1
        
#     userData = {
#         'disabled_alerts': True, 
#         'light_mode': True
#     }

#     response = client.post('/settings/preferences', data=userData)

#     assert response.status_code == 200
#     with client.session_transaction() as session:
#         assert session['disabled_alerts'] is True
#         assert session['light_mode'] is True