from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_response_401():
    payload = {
        'user_name': 'st2ring',
        'password': '123456'
        }
    response = client.post('/api/v1/users/login', json = payload)
    assert response.status_code == 401

def test_read_main():
    response = client.get('/')
    assert response.status_code == 202
    assert response.json() == {'message': 'Hello World!'}