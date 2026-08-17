import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Conversation, Message
from core.serializers import SymptomCheckRequestSerializer, ChatResponseSerializer
from core.services.ai_service import ai_service
from core.services.safety_service import safety_service
from core.services.rate_limiter import rate_limiter


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_symptoms(request):
    serializer = SymptomCheckRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    if rate_limiter.is_rate_limited(f"symptom_{request.user.id}"):
        return Response({'detail': 'Rate limit exceeded. Please wait.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    emergency_check = safety_service.check_emergency(
        f"{data['main_symptom']} {data['other_symptoms']}"
    )
    if emergency_check['is_emergency']:
        return Response({
            'reply': (
                "EMERGENCY DETECTED\n\n"
                "Based on the symptoms you've described, you may be experiencing a medical emergency.\n\n"
                "IMMEDIATE ACTIONS:\n"
                "1. Call emergency services immediately (911 / 112 / 999)\n"
                "2. Go to the nearest emergency room\n"
                "3. Do not drive yourself\n\n"
                "This AI system cannot provide emergency care. Please seek help immediately."
            ),
            'conversation_id': 0,
            'risk_level': 'emergency',
            'follow_up_questions': [],
            'safety_warnings': ['EMERGENCY: Seek immediate medical attention'],
            'is_emergency': True
        })

    symptom_data = {
        'main_symptom': data['main_symptom'],
        'duration': data['duration'],
        'severity': data['severity'],
        'age_group': data['age_group'],
        'existing_conditions': data['existing_conditions'],
        'medications': data['medications'],
        'other_symptoms': data['other_symptoms'],
        'triggers': data['triggers'],
    }

    ai_response = ai_service.analyze_symptoms(symptom_data)

    response_text = ai_response.get('response', 'Unable to analyze symptoms at this time.')
    risk_level = ai_response.get('risk_level', 'low')
    follow_ups = ai_response.get('follow_up_questions', [])

    conversation = Conversation.objects.create(
        user_id=request.user.id,
        title=f"Symptom Check: {data['main_symptom'][:60]}",
        category='symptom_check',
        risk_level=risk_level,
    )

    Message.objects.create(
        conversation_id=conversation.id,
        role='user',
        content=json.dumps(symptom_data),
    )

    Message.objects.create(
        conversation_id=conversation.id,
        role='assistant',
        content=response_text,
        risk_level=risk_level,
    )

    return Response({
        'reply': response_text,
        'conversation_id': conversation.id,
        'risk_level': risk_level,
        'follow_up_questions': follow_ups,
        'safety_warnings': ai_response.get('safety_warnings', []),
        'is_emergency': risk_level == 'emergency'
    })
