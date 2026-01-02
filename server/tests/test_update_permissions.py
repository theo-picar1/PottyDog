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
        
        
# Test to see if admin tries to do this with expired session
def test_session_missing_user_id(client):
    with client.session_transaction() as session:
        session.clear()
    
    response = client.post('/admin-dashboard/permissions', follow_redirects=True)
    
    assert b"Administrator Login" in response.data
        

# ----- BROKEN TEST -----  
# Test to see if non admin tries to do this
# @patch('app.get_db_connection')
# def test_update_permissions_unauthorised(mock_get_db_connection, client):
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_get_db_connection.return_value = mock_conn
#     mock_conn.cursor.return_value = mock_cursor
#     mock_cursor.fetchone.return_value = {
#         'id': 1,
#         'email': 'taskkshkashde@email.com',
#         'is_admin': False
#     }
    
#     with client.session_transaction() as session:
#         session['user_id'] = 1
#         session['is_admin'] = True
    
#     response = client.post('/admin-dashboard/permissions')
    
#     assert response.status_code == 401
    
    
# ----- BROKEN TEST -----  
# Test to see if admin can change permissions (multiple users)
# @patch('app.get_db_connection')
# def test_update_permissions_multiple_users(mock_get_db_connection, client):
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_get_db_connection.return_value = mock_conn
#     mock_conn.cursor.return_value = mock_cursor
#     mock_cursor.fetchone.return_value = {
#         'id': 1,
#         'email': 'theopic@email.com',
#         'is_admin': True
#     }
#     mock_cursor.fetchall.side_effect = [
#         [
#             {'id': 2, 'can_write': 1, 'can_read': 0},
#             {'id': 3, 'can_write': 0, 'can_read': 0},
#         ],
#         [
#             {'id': 2, 'can_write': 0, 'can_read': 1},
#             {'id': 3, 'can_write': 0, 'can_read': 1},
#         ]
#     ]
    
#     with client.session_transaction() as session:
#         session['user_id'] = 1
#         session['is_admin'] = True
        
#     response = client.post('/admin-dashboard/permissions')
        
#     assert response.status_code == 200
#     assert b"Successfully changed permissions of selected users!" in response.data
    

# ----- BROKEN TEST -----  
# Test to see if admin can change permissions (one user)
# @patch('app.get_db_connection')
# def test_update_permissions_one_user(mock_get_db_connection, client):
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_get_db_connection.return_value = mock_conn
#     mock_conn.cursor.return_value = mock_cursor
#     mock_cursor.fetchone.return_value = {
#         'id': 1,
#         'email': 'theopic@email.com',
#         'is_admin': True
#     }
#     mock_cursor.fetchall.side_effect = [
#         [
#             {'id': 2, 'can_write': 1, 'can_read': 1},
#             {'id': 3, 'can_write': 0, 'can_read': 0},
#         ],
#         [
#             {'id': 2, 'can_write': 1, 'can_read': 0},
#             {'id': 3, 'can_write': 0, 'can_read': 0},
#         ]
#     ]
    
#     with client.session_transaction() as session:
#         session['user_id'] = 1
#         session['is_admin'] = True
        
#     response = client.post('/admin-dashboard/permissions')
        
#     assert response.status_code == 200
#     assert b"Successfully changed permissions of selected user!" in response.data
    

# ----- BROKEN TEST -----  
# Test to see if admin saves changes but they did not make changes
# @patch('app.get_db_connection')
# def test_update_permissions_no_changes(mock_get_db_connection, client):
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_get_db_connection.return_value = mock_conn
#     mock_conn.cursor.return_value = mock_cursor
#     mock_cursor.fetchone.return_value = {
#         'id': 1,
#         'email': 'theopic@email.com',
#         'is_admin': True
#     }
#     mock_cursor.fetchall.side_effect = [
#         [
#             {'id': 2, 'can_write': 1, 'can_read': 1},
#             {'id': 3, 'can_write': 0, 'can_read': 0},
#         ],
#         [
#             {'id': 2, 'username': 'lalapic', 'can_write': 1, 'can_read': 1},
#             {'id': 3, 'username': 'piclala', 'can_write': 0, 'can_read': 0},
#         ]
#     ]
    
#     with client.session_transaction() as session:
#         session['user_id'] = 1
#         session['is_admin'] = True
        
#     response = client.post('/admin-dashboard/permissions')
        
#     assert response.status_code == 200
#     html = response.data.decode('utf-8')
#     assert b"No changes were made!" in html
    
    
# Test for 500 error
@patch('app.get_db_connection')
def test_server_error(mock_get_db_connection, client):
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