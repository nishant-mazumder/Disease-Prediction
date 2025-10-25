from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Doctor, ContactMessage


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'date_of_birth', 'address', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class DoctorSearchForm(forms.Form):
    SPECIALIZATION_CHOICES = [
        ('', 'All Specializations'),
        ('cardiology', 'Cardiology'),
        ('endocrinology', 'Endocrinology'),
        ('neurology', 'Neurology'),
        ('general', 'General Medicine'),
        ('pediatrics', 'Pediatrics'),
        ('dermatology', 'Dermatology'),
        ('orthopedics', 'Orthopedics'),
    ]

    specialization = forms.ChoiceField(
        choices=SPECIALIZATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'})
    )
    min_rating = forms.FloatField(
        required=False,
        min_value=0.0,
        max_value=5.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min rating', 'step': '0.1'})
    )
    max_fees = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max fees'})
    )


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


# Disease-specific prediction forms
class DiabetesPredictionForm(forms.Form):
    pregnancies = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    glucose = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    blood_pressure = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    skin_thickness = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    insulin = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    bmi = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    diabetes_pedigree_function = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class HeartDiseasePredictionForm(forms.Form):
    age = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    sex = forms.ChoiceField(
        choices=[(0, 'Female'), (1, 'Male')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cp = forms.IntegerField(
        min_value=0,
        max_value=3,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    trestbps = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    chol = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    fbs = forms.ChoiceField(
        choices=[(0, 'No'), (1, 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    restecg = forms.IntegerField(
        min_value=0,
        max_value=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    thalach = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    exang = forms.ChoiceField(
        choices=[(0, 'No'), (1, 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    oldpeak = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    slope = forms.IntegerField(
        min_value=0,
        max_value=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    ca = forms.IntegerField(
        min_value=0,
        max_value=3,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    thal = forms.IntegerField(
        min_value=0,
        max_value=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class ParkinsonsPredictionForm(forms.Form):
    fo = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    fhi = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    flo = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    jitter_percent = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    jitter_abs = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    rap = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    ppq = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    ddp = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    shimmer = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    shimmer_db = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    apq3 = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    apq5 = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    apq = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    dda = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    nhr = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    hnr = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    rpde = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    dfa = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    spread1 = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    spread2 = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    d2 = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    ppe = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
