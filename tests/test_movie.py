from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Helper functions


def login_test_user():
    form_data = {
        'username': 'movieuser',
        'password': 'password123'
    }
    response = client.post('/login/', data=form_data)
    return response.json()['access_token']


def get_test_move_id(token):
    response = client.get('/movies/search/?query=batman', headers={'Authorization': f"Bearer {token}"})
    return response.json()['films'][0]['filmId']


# Tests
def test_register():
    user_data = {
        'username': 'movieuser',
        'email': 'testmovie@example.com',
        'password': 'password123',
    }
    response = client.post('/register/', json=user_data)
    assert response.status_code == 201
    assert response.json()['username'] == 'movieuser'


def test_search_movie():
    token = login_test_user()
    response = client.get('/movies/search/?query=batman', headers={'Authorization': f"Bearer {token}"})
    assert len(response.json()['films']) > 0


def test_get_movie():
    token = login_test_user()
    id = get_test_move_id(token)
    response = client.get(f"/movies/{id}", headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 200
    assert 'kinopoiskId' in response.json()
    assert response.json()['kinopoiskId'] == id


def test_add_favorite():
    token = login_test_user()
    id = get_test_move_id(token)
    response = client.post(f"/movies/favorites/{id}", headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 201
    assert 'kinopoiskId' in response.json()
    assert len(response.json()) >= 0


def test_get_favorites():
    token = login_test_user()
    response = client.get('/movies/favorites/', headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) >= 0


def test_delete_favorite():
    token = login_test_user()
    id = get_test_move_id(token)
    response = client.delete(f"/movies/favorites/{id}", headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 204


def test_unauthorized_access():
    response = client.get('/movies/search/')
    assert response.status_code == 401


def test_empty_query():
    token = login_test_user()
    response = client.get('/movies/search/?query=', headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()['films']) == 0


def test_page_parameter():
    token = login_test_user()
    response = client.get('/movies/search/?query=batman&page=2', headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_invalid_page():
    token = login_test_user()
    response = client.get('/movies/search/?query=test&page=-1', headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 422


def test_nonexistent_movie():
    token = login_test_user()
    response = client.get('/movies/1', headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 404


def test_add_favorite_nonexistent():
    token = login_test_user()
    response = client.post('/movies/favorites/1', headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 404


def test_delete_nonexistent_favorite():
    token = login_test_user()
    response = client.delete('/movies/favorites/9999', headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 404
