from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from core.models import Conversation, Message
from core.serializers import (
    ConversationCreateSerializer, ConversationResponseSerializer,
    MessageResponseSerializer
)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_or_create_conversation(request):
    if request.method == 'GET':
        search = request.query_params.get('search')
        conversations = Conversation.objects.filter(user_id=request.user.id, is_active=True)
        if search:
            conversations = conversations.filter(title__icontains=search)
        conversations = conversations.order_by('-updated_at')
        return Response(ConversationResponseSerializer(conversations, many=True).data)

    serializer = ConversationCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    conversation = Conversation.objects.create(
        user_id=request.user.id,
        title=data['title'],
        category=data['category'],
    )
    return Response(ConversationResponseSerializer(conversation).data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def conversation_detail(request, conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id, user_id=request.user.id)
    except Conversation.DoesNotExist:
        return Response({'detail': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ConversationResponseSerializer(conversation).data)

    if request.method == 'DELETE':
        conversation.delete()
        return Response({'message': 'Conversation deleted'})

    title = request.data.get('title')
    if title:
        conversation.title = title
        conversation.save()
    return Response({'message': 'Conversation updated'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id, user_id=request.user.id)
    except Conversation.DoesNotExist:
        return Response({'detail': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

    messages = Message.objects.filter(conversation_id=conversation_id).order_by('created_at')
    return Response(MessageResponseSerializer(messages, many=True).data)
