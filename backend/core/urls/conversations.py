from django.urls import path
from ..views.conversations import (
    list_or_create_conversation, conversation_detail, get_messages
)

urlpatterns = [
    path('', list_or_create_conversation, name='list-or-create-conversation'),
    path('<int:conversation_id>/', conversation_detail, name='conversation-detail'),
    path('<int:conversation_id>/messages/', get_messages, name='get-messages'),
]
