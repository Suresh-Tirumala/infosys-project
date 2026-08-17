import pytest
import json


@pytest.mark.django_db
class TestChat:
    def test_chat_no_ai(self, client, auth_headers):
        response = client.post('/api/chat/',
            data=json.dumps({'message': 'I have a headache'}),
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert 'reply' in data
        assert 'conversation_id' in data
        assert 'risk_level' in data

    def test_chat_unauthenticated(self, client):
        response = client.post('/api/chat/',
            data=json.dumps({'message': 'Hello'}),
            content_type='application/json'
        )
        assert response.status_code == 401

    def test_chat_creates_conversation(self, client, auth_headers):
        response = client.post('/api/chat/',
            data=json.dumps({'message': 'I feel tired'}),
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        conv_id = json.loads(response.content)['conversation_id']
        assert conv_id > 0

    def test_chat_empty_message(self, client, auth_headers):
        response = client.post('/api/chat/',
            data=json.dumps({'message': ''}),
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestConversations:
    def test_list_conversations(self, client, auth_headers):
        response = client.get('/api/conversations/',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        assert response.status_code == 200
        assert isinstance(json.loads(response.content), list)

    def test_create_conversation(self, client, auth_headers):
        response = client.post('/api/conversations/',
            data=json.dumps({'title': 'Test conversation'}),
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        assert response.status_code == 200
        assert json.loads(response.content)['title'] == 'Test conversation'

    def test_delete_conversation(self, client, auth_headers):
        create = client.post('/api/conversations/',
            data=json.dumps({'title': 'To delete'}),
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        conv_id = json.loads(create.content)['id']
        response = client.delete(f'/api/conversations/{conv_id}/',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        assert response.status_code == 200
