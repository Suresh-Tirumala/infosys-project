from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.serializers import MedicationQuerySerializer
from core.services.ai_service import ai_service
from core.services.safety_service import safety_service


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_medication_info(request):
    serializer = MedicationQuerySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    if safety_service.detect_prompt_injection(data['question']):
        return Response({'response': 'Please ask your medication question in a straightforward way.'})

    result = ai_service.medication_info(data['question'])
    return Response({'response': result.get('response', 'Unable to provide information at this time.')})
