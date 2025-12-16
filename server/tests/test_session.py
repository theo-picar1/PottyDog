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
        'email': 'test@example.com',
        'password': bcrypt.generate_password_hash('CorrectPassword1!').decode('utf-8'),
        'username': 'DaDude',
        'dog_name': 'eaterOfWorlds'
    }

    data = {
        'email': 'test@example.com',
        'password': 'CorrectPassword1!'
    }

    # Login first to have logged-in version of index.html
    client.post('/login', data=data)

    response = client.get('/')

    assert response.status_code == 200
    assert b'DaDude' in response.data
    assert b'eaterOfWorlds' in response.data