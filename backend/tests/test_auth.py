import pytest
import json


@pytest.mark.django_db
class TestRegistration:
    def test_register_success(self, client):
        response = client.post('/api/auth/register/',
            data=json.dumps({
                'username': 'newuser',
                'email': 'new@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert 'access_token' in data
        assert data['user']['email'] == 'new@example.com'

    def test_register_duplicate_email(self, client, registered_user):
        response = client.post('/api/auth/register/',
            data=json.dumps({
                'username': 'another',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_register_short_password(self, client):
        response = client.post('/api/auth/register/',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': '12345'
            }),
            content_type='application/json'
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestLogin:
    def test_login_success(self, client, registered_user):
        response = client.post('/api/auth/login/',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert 'access_token' in json.loads(response.content)

    def test_login_wrong_password(self, client, registered_user):
        response = client.post('/api/auth/login/',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post('/api/auth/login/',
            data=json.dumps({
                'email': 'nonexistent@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        assert response.status_code == 401


@pytest.mark.django_db
class TestProtectedRoutes:
    def test_get_me_authenticated(self, client, auth_headers):
        response = client.get('/api/auth/me/', HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION'])
        assert response.status_code == 200
        assert json.loads(response.content)['email'] == 'test@example.com'

    def test_get_me_unauthenticated(self, client):
        response = client.get('/api/auth/me/')
        assert response.status_code == 401
