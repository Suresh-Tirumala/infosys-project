from django.urls import path
from ..views.chat import send_message

urlpatterns = [
    path('', send_message, name='send-message'),
]
