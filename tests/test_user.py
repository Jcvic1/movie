from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Helper functions


def login_test_user():
    form_data = {
        'username': 'testuser',
        'password': 'password123'
    }
    response = client.post('/login/', data=form_data)
    return response.json()['access_token']

# Test functions


def test_register():
    user_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'}
    response = client.post('/register/', json=user_data)
    assert response.status_code == 201
    assert response.json()['username'] == 'testuser'


def test_login():
    form_data = {
        'username': 'testuser',
        'password': 'password123'
    }
    response = client.post('/login/', data=form_data)
    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_register_invalid():
    invalid_data = {'username': '', 'email': 'invalid_email', 'password': ''}
    response = client.post('/register/', json=invalid_data)
    assert response.status_code == 422


def test_login_incorrect():
    form_data = {
        'username': 'nonexistent',
        'password': 'wrong'
    }
    response = client.post('/login/', data=form_data)
    assert response.status_code == 404


def test_unauthorized_fields():

    response = client.get('/profile/')
    assert response.status_code == 401


def test_profile():
    user_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'}
    response = client.post('/register/', json=user_data)
    form_data = {
        'username': 'testuser',
        'password': 'password123'
    }
    response = client.post('/login/', data=form_data)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    token = response.json()['access_token']

    response = client.get('/profile/', headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['username'] == user_data['username']
