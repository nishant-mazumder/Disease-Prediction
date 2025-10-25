from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import UserProfile, Doctor, Prediction, ContactMessage
from .forms import (
    UserRegistrationForm, UserProfileForm, DoctorSearchForm, 
    ContactForm, DiabetesPredictionForm, HeartDiseasePredictionForm, 
    ParkinsonsPredictionForm
)
from .ml_utils import predict_diabetes, predict_heart_disease, predict_parkinsons
from .chatbot_utils import get_chatbot
import json
from django.http import JsonResponse


def home(request):
    """Landing page view."""
    return render(request, 'home.html')


def about(request):
    """About page view."""
    return render(request, 'about.html')


def contact(request):
    """Contact page view."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email notification to admin
            try:
                send_mail(
                    f'New Contact Message: {contact_message.subject}',
                    f'From: {contact_message.name} ({contact_message.email})\n\n{contact_message.message}',
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                messages.warning(request, 'Message saved but email notification failed.')
            
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})


def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    """User login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')


def user_logout(request):
    """User logout view."""
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    """User dashboard view."""
    # Get user's recent predictions
    recent_predictions = Prediction.objects.filter(user=request.user)[:5]
    
    # Get user profile
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'recent_predictions': recent_predictions,
        'profile': profile,
    }
    return render(request, 'dashboard.html', context)


@login_required
def profile(request):
    """User profile view and edit."""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form, 'profile': profile})


def doctor_search(request):
    """Doctor search and listing view."""
    doctors = Doctor.objects.filter(is_available=True)
    form = DoctorSearchForm(request.GET)
    
    if form.is_valid():
        specialization = form.cleaned_data.get('specialization')
        location = form.cleaned_data.get('location')
        min_rating = form.cleaned_data.get('min_rating')
        max_fees = form.cleaned_data.get('max_fees')
        
        if specialization:
            doctors = doctors.filter(specialization=specialization)
        if location:
            doctors = doctors.filter(location__icontains=location)
        if min_rating is not None:
            doctors = doctors.filter(rating__gte=min_rating)
        if max_fees is not None:
            doctors = doctors.filter(fees__lte=max_fees)
    
    # Pagination
    paginator = Paginator(doctors, 6)
    page_number = request.GET.get('page')
    doctors = paginator.get_page(page_number)
    
    return render(request, 'doctor_search.html', {
        'doctors': doctors,
        'form': form,
    })


@login_required
def diabetes_prediction(request):
    """Diabetes prediction view."""
    if request.method == 'POST':
        form = DiabetesPredictionForm(request.POST)
        if form.is_valid():
            try:
                # Get prediction
                prediction_result = predict_diabetes(form.cleaned_data)
                
                # Save prediction to database
                Prediction.objects.create(
                    user=request.user,
                    disease_type='diabetes',
                    prediction_result=prediction_result['prediction'],
                    confidence_score=prediction_result['confidence'],
                    input_data=form.cleaned_data
                )
                
                return render(request, 'prediction_result.html', {
                    'disease_type': 'Diabetes',
                    'prediction_result': prediction_result,
                    'form': form
                })
            except Exception as e:
                messages.error(request, f'Prediction failed: {str(e)}')
    else:
        form = DiabetesPredictionForm()
    
    return render(request, 'diabetes_prediction.html', {'form': form})


@login_required
def heart_disease_prediction(request):
    """Heart disease prediction view."""
    if request.method == 'POST':
        form = HeartDiseasePredictionForm(request.POST)
        if form.is_valid():
            try:
                # Get prediction
                prediction_result = predict_heart_disease(form.cleaned_data)
                
                # Save prediction to database
                Prediction.objects.create(
                    user=request.user,
                    disease_type='heart_disease',
                    prediction_result=prediction_result['prediction'],
                    confidence_score=prediction_result['confidence'],
                    input_data=form.cleaned_data
                )
                
                return render(request, 'prediction_result.html', {
                    'disease_type': 'Heart Disease',
                    'prediction_result': prediction_result,
                    'form': form
                })
            except Exception as e:
                messages.error(request, f'Prediction failed: {str(e)}')
    else:
        form = HeartDiseasePredictionForm()
    
    return render(request, 'heart_disease_prediction.html', {'form': form})


@login_required
def parkinsons_prediction(request):
    """Parkinson's disease prediction view."""
    if request.method == 'POST':
        form = ParkinsonsPredictionForm(request.POST)
        if form.is_valid():
            try:
                # Get prediction
                prediction_result = predict_parkinsons(form.cleaned_data)
                
                # Save prediction to database
                Prediction.objects.create(
                    user=request.user,
                    disease_type='parkinsons',
                    prediction_result=prediction_result['prediction'],
                    confidence_score=prediction_result['confidence'],
                    input_data=form.cleaned_data
                )
                
                return render(request, 'prediction_result.html', {
                    'disease_type': 'Parkinson\'s Disease',
                    'prediction_result': prediction_result,
                    'form': form
                })
            except Exception as e:
                messages.error(request, f'Prediction failed: {str(e)}')
    else:
        form = ParkinsonsPredictionForm()
    
    return render(request, 'parkinsons_prediction.html', {'form': form})


@login_required
def prediction_history(request):
    """User's prediction history view."""
    predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(predictions, 10)
    page_number = request.GET.get('page')
    predictions = paginator.get_page(page_number)
    
    return render(request, 'prediction_history.html', {'predictions': predictions})


@login_required
def make_prediction(request):
    """Generic prediction view for all diseases."""
    if request.method == 'POST':
        disease_type = request.POST.get('disease_type')
        
        if disease_type == 'diabetes':
            form = DiabetesPredictionForm(request.POST)
        elif disease_type == 'heart_disease':
            form = HeartDiseasePredictionForm(request.POST)
        elif disease_type == 'parkinsons':
            form = ParkinsonsPredictionForm(request.POST)
        else:
            messages.error(request, 'Invalid disease type.')
            return redirect('dashboard')
        
        if form.is_valid():
            try:
                form_data = form.cleaned_data
                
                prediction = Prediction(
                    user=request.user,
                    disease_type=disease_type,
                    input_data=form_data
                )
                
                # Preprocess the data before prediction
                processed_data = prediction.preprocess_input_data()
                
                # Use existing prediction utilities based on disease_type
                if disease_type == 'diabetes':
                    result = predict_diabetes(processed_data)
                elif disease_type == 'heart_disease':
                    result = predict_heart_disease(processed_data)
                elif disease_type == 'parkinsons':
                    result = predict_parkinsons(processed_data)
                else:
                    raise ValueError('Unsupported disease type for prediction.')
                
                # Expecting result as dict with 'prediction' and 'confidence'
                prediction.prediction_result = result['prediction']
                prediction.confidence_score = result['confidence']
                prediction.save()
                
                messages.success(request, 'Prediction made successfully!')
                return redirect('prediction_history')
            except Exception as e:
                messages.error(request, f'Prediction failed: {str(e)}')
    else:
        form = DiabetesPredictionForm()  # Default form, can be any
    
    return render(request, 'make_prediction.html', {'form': form})


def chatbot_page(request):
    """Chatbot page view."""
    return render(request, 'chatbot.html')


def chatbot_api(request):
    """Chatbot API endpoint for AJAX requests."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            session_key = data.get('session_key', '')
            
            # Get or create session data
            if 'chatbot_session' not in request.session:
                request.session['chatbot_session'] = {
                    'symptoms': [],
                    'conversation_stage': 'initial',
                    'user_info': {},
                    'current_disease': None,
                    'confidence': 0
                }
            
            session_data = request.session['chatbot_session']
            chatbot = get_chatbot()
            
            if not chatbot.model:
                return JsonResponse({
                    'response': 'Sorry, the chatbot is currently unavailable. Please try again later.',
                    'type': 'error'
                })
            
            # Process the message based on conversation stage
            if session_data['conversation_stage'] == 'initial':
                # Extract symptoms from initial message
                symptoms = chatbot.extract_symptoms(message)
                if symptoms:
                    session_data['symptoms'] = symptoms
                    session_data['conversation_stage'] = 'symptoms_confirmed'
                    
                    # Get initial prediction
                    disease, confidence, _ = chatbot.predict_disease(symptoms)
                    session_data['current_disease'] = disease
                    session_data['confidence'] = confidence
                    
                    # Get related symptoms to ask about
                    related_symptoms = chatbot.get_related_symptoms(disease, symptoms)
                    session_data['related_symptoms'] = related_symptoms[:5]  # Limit to 5 questions
                    session_data['current_question'] = 0
                    
                    response = f"✅ I detected these symptoms: {', '.join(symptoms)}\n\n"
                    response += f"🤖 Based on your symptoms, you might have **{disease}** (Confidence: {confidence}%)\n\n"
                    response += f"📖 About {disease}: {chatbot.get_disease_description(disease)}\n\n"
                    
                    if related_symptoms:
                        response += f"Let me ask you a few more questions to get a more accurate diagnosis:\n"
                        response += f"👉 Do you also have {related_symptoms[0].replace('_', ' ')}? (yes/no)"
                    else:
                        response += "I have enough information to provide you with a diagnosis and recommendations."
                        session_data['conversation_stage'] = 'complete'
                        
                else:
                    response = "❌ I couldn't detect any specific symptoms in your message. Please describe your symptoms more clearly (e.g., 'I have fever and headache')."
                    
            elif session_data['conversation_stage'] == 'symptoms_confirmed':
                # Process yes/no answers for related symptoms
                answer = message.lower().strip()
                related_symptoms = session_data.get('related_symptoms', [])
                current_question = session_data.get('current_question', 0)
                
                if answer in ['yes', 'y', 'true', '1']:
                    session_data['symptoms'].append(related_symptoms[current_question])
                
                # Move to next question or complete
                current_question += 1
                session_data['current_question'] = current_question
                
                if current_question < len(related_symptoms):
                    response = f"👉 Do you also have {related_symptoms[current_question].replace('_', ' ')}? (yes/no)"
                else:
                    # Final prediction
                    disease, confidence, _ = chatbot.predict_disease(session_data['symptoms'])
                    session_data['current_disease'] = disease
                    session_data['confidence'] = confidence
                    session_data['conversation_stage'] = 'complete'
                    
                    response = f"🎯 **Final Diagnosis**: {disease} (Confidence: {confidence}%)\n\n"
                    response += f"📖 **About {disease}**: {chatbot.get_disease_description(disease)}\n\n"
                    
                    precautions = chatbot.get_disease_precautions(disease)
                    if precautions:
                        response += "🛡️ **Recommended Precautions**:\n"
                        for i, prec in enumerate(precautions, 1):
                            response += f"{i}. {prec}\n"
                        response += "\n"
                    
                    response += f"💡 {chatbot.get_random_quote()}\n\n"
                    response += "⚠️ **Important**: This is an AI-powered assessment and should not replace professional medical advice. Please consult a healthcare provider for proper diagnosis and treatment."
                    
            elif session_data['conversation_stage'] == 'complete':
                # Reset conversation
                request.session['chatbot_session'] = {
                    'symptoms': [],
                    'conversation_stage': 'initial',
                    'user_info': {},
                    'current_disease': None,
                    'confidence': 0
                }
                response = "🔄 Starting a new consultation. Please describe your symptoms (e.g., 'I have fever and headache')."
            
            else:
                response = "I'm not sure how to help with that. Please describe your symptoms clearly."
            
            # Save session data
            request.session.save()
            
            return JsonResponse({
                'response': response,
                'type': 'success'
            })
            
        except Exception as e:
            return JsonResponse({
                'response': f'Sorry, there was an error processing your request: {str(e)}',
                'type': 'error'
            })
    
    return JsonResponse({
        'response': 'Invalid request method',
        'type': 'error'
    })


def reset_chatbot(request):
    """Reset chatbot session."""
    if 'chatbot_session' in request.session:
        del request.session['chatbot_session']
    return JsonResponse({'status': 'success'})
