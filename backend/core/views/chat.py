import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import User, HealthProfile, Conversation, Message
from core.serializers import ChatRequestSerializer, ChatResponseSerializer
from core.services.ai_service import ai_service
from core.services.safety_service import safety_service
from core.services.rate_limiter import rate_limiter


def get_health_context(user, db=None):
    try:
        profile = HealthProfile.objects.get(user_id=user.id)
    except HealthProfile.DoesNotExist:
        return ""
    parts = []
    if profile.age:
        parts.append(f"Age: {profile.age}")
    if profile.sex:
        parts.append(f"Sex: {profile.sex}")
    if profile.existing_conditions:
        parts.append(f"Conditions: {profile.existing_conditions}")
    if profile.current_medications:
        parts.append(f"Medications: {profile.current_medications}")
    if profile.allergies:
        parts.append(f"Allergies: {profile.allergies}")
    return "; ".join(parts)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    serializer = ChatRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    if rate_limiter.is_rate_limited(f"user_{request.user.id}"):
        return Response({'detail': 'Rate limit exceeded. Please wait.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    if safety_service.detect_prompt_injection(data['message']):
        return Response({
            'reply': 'I noticed something unusual in your message. Please describe your health concern in your own words.',
            'conversation_id': 0,
            'risk_level': 'low',
            'follow_up_questions': [],
            'safety_warnings': [],
            'is_emergency': False
        })

    emergency_check = safety_service.check_emergency(data['message'])
    if emergency_check['is_emergency']:
        ai_emergency = ai_service.check_emergency(data['message'])
        return Response({
            'reply': (
                "EMERGENCY DETECTED\n\n"
                "Based on your description, you may be experiencing a medical emergency.\n\n"
                "IMMEDIATE ACTIONS:\n"
                "1. Call emergency services immediately (911 / 112 / 999)\n"
                "2. If possible, go to the nearest emergency room\n"
                "3. Do not drive yourself - call for help\n\n"
                "This is an AI system and cannot provide emergency care. "
                "Please seek professional medical help immediately."
            ),
            'conversation_id': data.get('conversation_id') or 0,
            'risk_level': 'emergency',
            'follow_up_questions': [],
            'safety_warnings': ['EMERGENCY: Seek immediate medical attention'],
            'is_emergency': True
        })

    conversation_id = data.get('conversation_id')
    if conversation_id:
        try:
            conversation = Conversation.objects.get(id=conversation_id, user_id=request.user.id)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        title = data['message'][:80] + ("..." if len(data['message']) > 80 else "")
        conversation = Conversation.objects.create(user_id=request.user.id, title=title)

    Message.objects.create(
        conversation_id=conversation.id,
        role='user',
        content=data['message'],
    )

    messages = list(Message.objects.filter(conversation_id=conversation.id).order_by('created_at'))
    chat_messages = [{'role': m.role, 'content': m.content} for m in messages]

    health_context = get_health_context(request.user)
    ai_response = ai_service.general_health_chat(chat_messages, health_context)

    response_text = ai_response.get('response', "I'm sorry, I couldn't process that request.")
    risk_level = ai_response.get('risk_level', 'low')
    follow_ups = ai_response.get('follow_up_questions', [])
    safety_warnings = ai_response.get('safety_warnings', [])

    safety_check = safety_service.validate_ai_response(response_text, data['message'])
    if not safety_check['is_safe']:
        response_text = safety_check['modified_response']
        safety_warnings.extend(safety_check['warnings'])

    Message.objects.create(
        conversation_id=conversation.id,
        role='assistant',
        content=response_text,
        risk_level=risk_level,
        metadata_json=json.dumps({
            'follow_up_questions': follow_ups,
            'safety_warnings': safety_warnings,
        })
    )

    if risk_level in ('high', 'emergency'):
        conversation.risk_level = risk_level
        conversation.save()

    return Response({
        'reply': response_text,
        'conversation_id': conversation.id,
        'risk_level': risk_level,
        'follow_up_questions': follow_ups,
        'safety_warnings': safety_warnings,
        'is_emergency': risk_level == 'emergency'
    })
