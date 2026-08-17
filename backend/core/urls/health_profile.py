from django.urls import path
from ..views.health_profile import health_profile_view

urlpatterns = [
    path('', health_profile_view, name='health-profile'),
]
