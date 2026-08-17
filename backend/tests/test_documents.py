import pytest
import json
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestDocumentUpload:
    def test_upload_text_file(self, client, auth_headers):
        content = b"Blood Test Report\nHemoglobin: 14.2 g/dL\nWBC: 7000"
        file = SimpleUploadedFile("report.txt", content, content_type="text/plain")
        response = client.post('/api/documents/upload/',
            data={'file': file},
            format='multipart',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['original_filename'] == 'report.txt'
        assert data['status'] == 'completed'

    def test_upload_invalid_type(self, client, auth_headers):
        file = SimpleUploadedFile("file.exe", b"test content", content_type="application/x-executable")
        response = client.post('/api/documents/upload/',
            data={'file': file},
            format='multipart',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        assert response.status_code == 400

    def test_list_documents(self, client, auth_headers):
        response = client.get('/api/documents/',
            HTTP_AUTHORIZATION=auth_headers['HTTP_AUTHORIZATION']
        )
        assert response.status_code == 200
        assert isinstance(json.loads(response.content), list)

    def test_upload_unauthenticated(self, client):
        file = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")
        response = client.post('/api/documents/upload/',
            data={'file': file},
            format='multipart'
        )
        assert response.status_code == 401
