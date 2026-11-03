def test_login_response_401(anon_client):
    payload = {
        'user_name': 'string',
        'password': '123456'
        }
    response = anon_client.post('/api/v1/users/login', json = payload)
    assert response.status_code == 401

def test_login_response_200(anon_client):
    payload = {
        'user_name': 'usertest',
        'password': '12345678910'
        }
    response = anon_client.post('/api/v1/users/login', json = payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_register_response_201(anon_client):
    payload = {
        'user_name': 'st2ring',
        'password': '123456',
        'password_confirm': '123456'
        }
    response = anon_client.post('/api/v1/users/register', json = payload)
    assert response.status_code == 201

def test_read_main(anon_client):
    response = anon_client.get('/')
    assert response.status_code == 202
    assert response.json() == {'message': 'Hello World!'}