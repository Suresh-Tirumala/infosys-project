import os
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from core.models import UserSettings, Conversation, Message, UploadedDocument, ReportSummary
from core.serializers import SettingsUpdateSerializer


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def settings_view(request):
    settings_obj, created = UserSettings.objects.get_or_create(user_id=request.user.id)

    if request.method == 'GET':
        return Response({
            'language': settings_obj.language,
            'theme': settings_obj.theme,
            'voice_enabled': settings_obj.voice_enabled,
            'notification_enabled': settings_obj.notification_enabled,
            'data_retention_days': settings_obj.data_retention_days,
            'share_analytics': settings_obj.share_analytics,
        })

    serializer = SettingsUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    for key, value in data.items():
        if value is not None:
            setattr(settings_obj, key, value)

    settings_obj.save()
    return Response({'message': 'Settings updated'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_all_conversations(request):
    conversations = Conversation.objects.filter(user_id=request.user.id)
    for conv in conversations:
        Message.objects.filter(conversation_id=conv.id).delete()
        conv.delete()
    return Response({'message': 'All conversations deleted'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_all_data(request):
    docs = UploadedDocument.objects.filter(user_id=request.user.id)
    for doc in docs:
        filepath = os.path.join(settings.UPLOAD_DIR, doc.filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    ReportSummary.objects.filter(user_id=request.user.id).delete()
    UploadedDocument.objects.filter(user_id=request.user.id).delete()

    conversations = Conversation.objects.filter(user_id=request.user.id)
    for conv in conversations:
        Message.objects.filter(conversation_id=conv.id).delete()
        conv.delete()

    return Response({'message': 'All data deleted successfully'})
