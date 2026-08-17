from django.urls import path
from ..views.settings import settings_view, delete_all_conversations, delete_all_data

urlpatterns = [
    path('', settings_view, name='settings'),
    path('conversations/', delete_all_conversations, name='delete-all-conversations'),
    path('data/', delete_all_data, name='delete-all-data'),
]
