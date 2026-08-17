from django.urls import path
from ..views.medication import get_medication_info

urlpatterns = [
    path('info/', get_medication_info, name='medication-info'),
]
