import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        'status': 'ok',
        'app': 'HealthChat AI',
        'version': '1.0.0',
        'ai_configured': settings.GROQ_API_KEY is not None,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_health_categories(request):
    return Response({
        'categories': [
            {'id': 'fever', 'name': 'Fever', 'icon': 'thermometer', 'description': 'Temperature-related concerns'},
            {'id': 'headache', 'name': 'Headache', 'icon': 'brain', 'description': 'Head pain and migraines'},
            {'id': 'cold-flu', 'name': 'Cold & Flu', 'icon': 'snowflake', 'description': 'Respiratory infections'},
            {'id': 'cough', 'name': 'Cough', 'icon': 'wind', 'description': 'Cough and throat issues'},
            {'id': 'stomach', 'name': 'Stomach Problems', 'icon': 'stomach', 'description': 'Digestive concerns'},
            {'id': 'skin', 'name': 'Skin Problems', 'icon': 'skin', 'description': 'Skin conditions and rashes'},
            {'id': 'allergies', 'name': 'Allergies', 'icon': 'flower', 'description': 'Allergic reactions'},
            {'id': 'sleep', 'name': 'Sleep', 'icon': 'moon', 'description': 'Sleep-related issues'},
            {'id': 'nutrition', 'name': 'Nutrition', 'icon': 'apple', 'description': 'Diet and nutrition guidance'},
            {'id': 'mental', 'name': 'Mental Wellbeing', 'icon': 'heart', 'description': 'Mental health support'},
            {'id': 'womens', 'name': "Women's Health", 'icon': 'female', 'description': "Women's health concerns"},
            {'id': 'mens', 'name': "Men's Health", 'icon': 'male', 'description': "Men's health concerns"},
            {'id': 'children', 'name': "Children's Health", 'icon': 'child', 'description': 'Pediatric health concerns'},
            {'id': 'general', 'name': 'General Health', 'icon': 'activity', 'description': 'General health questions'},
        ]
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def root(request):
    return Response({
        'name': 'HealthChat AI',
        'version': '1.0.0',
        'docs': '/docs',
        'api': '/api',
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('core.urls.auth')),
    path('api/chat/', include('core.urls.chat')),
    path('api/conversations/', include('core.urls.conversations')),
    path('api/symptoms/', include('core.urls.symptoms')),
    path('api/health-profile/', include('core.urls.health_profile')),
    path('api/documents/', include('core.urls.documents')),
    path('api/reports/', include('core.urls.reports')),
    path('api/settings/', include('core.urls.settings')),
    path('api/medication/', include('core.urls.medication')),
    path('api/health/', health_check, name='health-check'),
    path('api/categories/', get_health_categories, name='health-categories'),
    path('', root, name='root'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
