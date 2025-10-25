from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from sklearn.preprocessing import LabelEncoder
import numpy as np


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('endocrinology', 'Endocrinology'),
        ('neurology', 'Neurology'),
        ('general', 'General Medicine'),
        ('pediatrics', 'Pediatrics'),
        ('dermatology', 'Dermatology'),
        ('orthopedics', 'Orthopedics'),
    ]

    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    location = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    experience_years = models.PositiveIntegerField()
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='doctor_pics/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

    class Meta:
        ordering = ['-rating', 'name']


class Prediction(models.Model):
    DISEASE_CHOICES = [
        ('diabetes', 'Diabetes'),
        ('heart_disease', 'Heart Disease'),
        ('parkinsons', 'Parkinson\'s Disease'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disease_type = models.CharField(max_length=50, choices=DISEASE_CHOICES)
    prediction_result = models.CharField(max_length=100)
    confidence_score = models.FloatField()
    input_data = models.JSONField()  # Store the input parameters used for prediction
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.disease_type} - {self.prediction_result}"

    def preprocess_input_data(self):
        """Preprocess input data before prediction"""
        data = self.input_data
        numeric_data = {}
        
        # Convert string values to numeric
        for key, value in data.items():
            try:
                numeric_data[key] = float(value)
            except (ValueError, TypeError):
                # For categorical variables, use label encoding
                le = LabelEncoder()
                if isinstance(value, (list, tuple)):
                    numeric_data[key] = le.fit_transform([str(v) for v in value])[0]
                else:
                    numeric_data[key] = le.fit_transform([str(value)])[0]
        
        return np.array(list(numeric_data.values())).reshape(1, -1)

    class Meta:
        ordering = ['-created_at']


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
