from rest_framework import serializers
from .models import User, HealthProfile, Conversation, Message, UploadedDocument, ReportSummary, UserSettings


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    first_name = serializers.CharField(required=False, default='')
    last_name = serializers.CharField(required=False, default='')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'created_at')


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    token_type = serializers.CharField(default='bearer')
    user = UserResponseSerializer()


class HealthProfileCreateSerializer(serializers.Serializer):
    age = serializers.IntegerField(required=False, allow_null=True, min_value=0, max_value=150)
    sex = serializers.CharField(required=False, allow_null=True)
    height = serializers.FloatField(required=False, allow_null=True, min_value=0, max_value=300)
    weight = serializers.FloatField(required=False, allow_null=True, min_value=0, max_value=500)
    blood_type = serializers.CharField(required=False, allow_null=True)
    allergies = serializers.CharField(required=False, default='')
    existing_conditions = serializers.CharField(required=False, default='')
    current_medications = serializers.CharField(required=False, default='')
    emergency_contact = serializers.CharField(required=False, default='')


class HealthProfileResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProfile
        fields = ('id', 'user_id', 'age', 'sex', 'height', 'weight', 'blood_type',
                  'allergies', 'existing_conditions', 'current_medications',
                  'emergency_contact', 'created_at', 'updated_at')


class ConversationCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, default='New Conversation')
    category = serializers.CharField(required=False, default='general')


class ConversationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ('id', 'user_id', 'title', 'category', 'risk_level', 'is_active',
                  'created_at', 'updated_at')


class MessageCreateSerializer(serializers.Serializer):
    content = serializers.CharField(min_length=1)
    language = serializers.CharField(required=False, default='en')


class MessageResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'conversation_id', 'role', 'content', 'risk_level', 'created_at')


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(min_length=1)
    conversation_id = serializers.IntegerField(required=False, allow_null=True)
    language = serializers.CharField(required=False, default='en')


class ChatResponseSerializer(serializers.Serializer):
    reply = serializers.CharField()
    conversation_id = serializers.IntegerField()
    risk_level = serializers.CharField()
    follow_up_questions = serializers.ListField(child=serializers.CharField(), default=[])
    safety_warnings = serializers.ListField(child=serializers.CharField(), default=[])
    is_emergency = serializers.BooleanField(default=False)


class SymptomCheckRequestSerializer(serializers.Serializer):
    main_symptom = serializers.CharField()
    duration = serializers.CharField(required=False, default='', allow_blank=True)
    severity = serializers.CharField(required=False, default='', allow_blank=True)
    age_group = serializers.CharField(required=False, default='', allow_blank=True)
    existing_conditions = serializers.CharField(required=False, default='', allow_blank=True)
    medications = serializers.CharField(required=False, default='', allow_blank=True)
    other_symptoms = serializers.CharField(required=False, default='', allow_blank=True)
    triggers = serializers.CharField(required=False, default='', allow_blank=True)


class DocumentUploadResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDocument
        fields = ('id', 'filename', 'original_filename', 'file_type', 'file_size',
                  'summary', 'status', 'created_at')


class ReportSummaryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSummary
        fields = ('id', 'user_id', 'conversation_id', 'symptoms_mentioned', 'duration',
                  'key_info', 'questions_discussed', 'guidance', 'warning_signs',
                  'next_steps', 'created_at')


class SettingsUpdateSerializer(serializers.Serializer):
    language = serializers.CharField(required=False)
    theme = serializers.CharField(required=False)
    voice_enabled = serializers.BooleanField(required=False)
    notification_enabled = serializers.BooleanField(required=False)
    data_retention_days = serializers.IntegerField(required=False)
    share_analytics = serializers.BooleanField(required=False)


class MedicationQuerySerializer(serializers.Serializer):
    question = serializers.CharField()
    language = serializers.CharField(required=False, default='en')
