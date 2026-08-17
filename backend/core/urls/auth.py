from django.urls import path
from ..views.auth import register, login, me_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('me/', me_view, name='me'),
]
