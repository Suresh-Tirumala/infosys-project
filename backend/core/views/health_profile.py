from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import HealthProfile
from core.serializers import HealthProfileCreateSerializer, HealthProfileResponseSerializer


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def health_profile_view(request):
    if request.method == 'GET':
        profile, created = HealthProfile.objects.get_or_create(user_id=request.user.id)
        return Response(HealthProfileResponseSerializer(profile).data)

    if request.method == 'DELETE':
        try:
            profile = HealthProfile.objects.get(user_id=request.user.id)
            profile.delete()
        except HealthProfile.DoesNotExist:
            pass
        return Response({'message': 'Health profile deleted'})

    profile, created = HealthProfile.objects.get_or_create(user_id=request.user.id)

    serializer = HealthProfileCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    for key, value in data.items():
        if value is not None:
            setattr(profile, key, value)

    profile.save()
    return Response(HealthProfileResponseSerializer(profile).data)
