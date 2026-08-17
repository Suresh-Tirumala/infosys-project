from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'


class HealthProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_profile')
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=20, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    blood_type = models.CharField(max_length=5, null=True, blank=True)
    allergies = models.TextField(default='')
    existing_conditions = models.TextField(default='')
    current_medications = models.TextField(default='')
    emergency_contact = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'health_profiles'


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255, default='New Conversation')
    category = models.CharField(max_length=50, default='general')
    risk_level = models.CharField(max_length=20, default='low')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversations'


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20)
    content = models.TextField()
    risk_level = models.CharField(max_length=20, default='low')
    metadata_json = models.TextField(default='{}')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'


class UploadedDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    filename = models.CharField(max_length=255)
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField(default=0)
    extracted_text = models.TextField(default='')
    summary = models.TextField(default='')
    status = models.CharField(max_length=20, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'uploaded_documents'


class ReportSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    conversation = models.ForeignKey(Conversation, on_delete=models.SET_NULL, null=True, blank=True)
    symptoms_mentioned = models.TextField(default='')
    duration = models.CharField(max_length=100, default='')
    key_info = models.TextField(default='')
    questions_discussed = models.TextField(default='')
    guidance = models.TextField(default='')
    warning_signs = models.TextField(default='')
    next_steps = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'report_summaries'


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    language = models.CharField(max_length=10, default='en')
    theme = models.CharField(max_length=20, default='light')
    voice_enabled = models.BooleanField(default=False)
    notification_enabled = models.BooleanField(default=True)
    data_retention_days = models.IntegerField(default=90)
    share_analytics = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_settings'
