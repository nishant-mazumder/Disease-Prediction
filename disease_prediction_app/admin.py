from django.contrib import admin
from .models import UserProfile, Doctor, Prediction, ContactMessage


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'location', 'rating', 'fees', 'is_available']
    list_filter = ['specialization', 'location', 'is_available', 'rating']
    search_fields = ['name', 'specialization', 'location']
    ordering = ['-rating', 'name']


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'disease_type', 'prediction_result', 'confidence_score', 'created_at']
    list_filter = ['disease_type', 'created_at', 'prediction_result']
    search_fields = ['user__username', 'disease_type']
    ordering = ['-created_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    ordering = ['-created_at']
