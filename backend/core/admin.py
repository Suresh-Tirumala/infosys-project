from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, HealthProfile, Conversation, Message, UploadedDocument, ReportSummary, UserSettings


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(HealthProfile)
class HealthProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'sex', 'blood_type')
    search_fields = ('user__email',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'risk_level', 'created_at')
    list_filter = ('category', 'risk_level')
    search_fields = ('title',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'role', 'created_at')
    list_filter = ('role',)


@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'user', 'file_type', 'status', 'created_at')
    list_filter = ('status', 'file_type')


@admin.register(ReportSummary)
class ReportSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'theme')
