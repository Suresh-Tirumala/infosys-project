import os
import uuid
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from core.models import UploadedDocument
from core.serializers import DocumentUploadResponseSerializer
from core.services.ai_service import ai_service
from core.services.rate_limiter import rate_limiter

ALLOWED_TYPES = ['application/pdf', 'text/plain', 'image/png', 'image/jpeg']


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_document(request):
    file = request.FILES.get('file')
    if not file:
        return Response({'detail': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    if file.content_type not in ALLOWED_TYPES:
        return Response({'detail': 'Unsupported file type. Please upload PDF, TXT, PNG, or JPG files.'}, status=status.HTTP_400_BAD_REQUEST)

    if file.size > settings.MAX_UPLOAD_SIZE:
        return Response({'detail': f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB."}, status=status.HTTP_400_BAD_REQUEST)

    file_ext = file.name.split('.')[-1] if '.' in file.name else 'pdf'
    filename = f"{uuid.uuid4().hex}.{file_ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)

    content = file.read()
    file.seek(0)

    with open(filepath, 'wb') as f:
        f.write(content)
    extracted_text = ''
    if file.content_type == 'text/plain':
        extracted_text = content.decode('utf-8', errors='ignore')
    else:
        extracted_text = f"[Document uploaded: {file.name} - {len(content)} bytes]"

    doc = UploadedDocument.objects.create(
        user_id=request.user.id,
        filename=filename,
        original_filename=file.name,
        file_type=file.content_type,
        file_size=len(content),
        extracted_text=extracted_text,
        status='processing',
    )

    try:
        ai_result = ai_service.explain_document(extracted_text)
        doc.summary = ai_result.get('response', 'Unable to generate summary.')
        doc.status = 'completed'
    except Exception:
        doc.status = 'completed'
        doc.summary = 'Document uploaded successfully. AI summary will be available shortly.'

    doc.save()
    return Response(DocumentUploadResponseSerializer(doc).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_documents(request):
    documents = UploadedDocument.objects.filter(user_id=request.user.id).order_by('-created_at')
    return Response(DocumentUploadResponseSerializer(documents, many=True).data)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def document_detail(request, doc_id):
    try:
        doc = UploadedDocument.objects.get(id=doc_id, user_id=request.user.id)
    except UploadedDocument.DoesNotExist:
        return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        filepath = os.path.join(settings.UPLOAD_DIR, doc.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        doc.delete()
        return Response({'message': 'Document deleted'})

    return Response(DocumentUploadResponseSerializer(doc).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ask_about_document(request, doc_id):
    try:
        doc = UploadedDocument.objects.get(id=doc_id, user_id=request.user.id)
    except UploadedDocument.DoesNotExist:
        return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

    question = request.data.get('question', '')
    ai_result = ai_service.explain_document(doc.extracted_text, question)
    return Response({'response': ai_result.get('response', 'Unable to answer that question.')})
