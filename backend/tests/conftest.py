import pytest
import json
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def registered_user(client, db):
    response = client.post('/api/auth/register/',
        data=json.dumps({
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
        }),
        content_type='application/json'
    )
    return json.loads(response.content)


@pytest.fixture
def auth_headers(registered_user):
    return {'HTTP_AUTHORIZATION': f"Bearer {registered_user['access_token']}"}
