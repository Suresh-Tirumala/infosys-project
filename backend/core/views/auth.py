from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from core.models import User, HealthProfile
from core.serializers import (
    UserCreateSerializer, UserLoginSerializer,
    UserResponseSerializer, TokenSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
    )
    user.set_password(data['password'])
    user.save()

    HealthProfile.objects.create(user=user)

    refresh = RefreshToken.for_user(user)
    token_data = {
        'access_token': str(refresh.access_token),
        'token_type': 'bearer',
        'user': UserResponseSerializer(user).data,
    }
    return Response(token_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    user = authenticate(email=data['email'], password=data['password'])
    if user is None:
        return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    token_data = {
        'access_token': str(refresh.access_token),
        'token_type': 'bearer',
        'user': UserResponseSerializer(user).data,
    }
    return Response(token_data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def me_view(request):
    if request.method == 'GET':
        return Response(UserResponseSerializer(request.user).data)

    if request.method == 'DELETE':
        request.user.is_active = False
        request.user.save()
        return Response({'message': 'Account deactivated successfully'})

    user = request.user
    if 'first_name' in request.data:
        user.first_name = request.data['first_name']
    if 'last_name' in request.data:
        user.last_name = request.data['last_name']
    user.save()
    return Response(UserResponseSerializer(user).data)
