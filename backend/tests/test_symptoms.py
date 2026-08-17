import pytest
import json


@pytest.mark.django_db
class TestSymptomChecker:
    def test_symptom_check_basic(self, client, auth_headers):
        response = client.post('/api/symptoms/check/',
            data=json.dumps({
                'main_symptom': 'headache',
                'duration': '1-2 days',
                'severity': 'mild',
                'age_group': 'adult (18-64)'
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert 'reply' in data
        assert 'risk_level' in data

    def test_symptom_check_minimal(self, client, auth_headers):
        response = client.post('/api/symptoms/check/',
            data=json.dumps({'main_symptom': 'cough'}),
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        assert response.status_code == 200

    def test_symptom_check_unauthenticated(self, client):
        response = client.post('/api/symptoms/check/',
            data=json.dumps({'main_symptom': 'fever'}),
            content_type='application/json'
        )
        assert response.status_code == 401


@pytest.mark.django_db
class TestEmergencyDetection:
    def test_emergency_keywords_detected(self, client, auth_headers):
        response = client.post('/api/chat/',
            data=json.dumps({'message': "I'm having chest pain and can't breathe"}),
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['is_emergency'] == True
        assert data['risk_level'] == 'emergency'

    def test_non_emergency_normal(self, client, auth_headers):
        response = client.post('/api/chat/',
            data=json.dumps({'message': 'I have a mild headache'}),
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['is_emergency'] == False
