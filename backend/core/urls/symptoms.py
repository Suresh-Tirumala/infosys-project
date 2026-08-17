from django.urls import path
from ..views.symptoms import check_symptoms

urlpatterns = [
    path('check/', check_symptoms, name='check-symptoms'),
]
