from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # User dashboard and profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Doctor search
    path('doctors/', views.doctor_search, name='doctor_search'),
    
    # Disease predictions
    path('predict/diabetes/', views.diabetes_prediction, name='diabetes_prediction'),
    path('predict/heart-disease/', views.heart_disease_prediction, name='heart_disease_prediction'),
    path('predict/parkinsons/', views.parkinsons_prediction, name='parkinsons_prediction'),
    
    # Prediction history
    path('prediction-history/', views.prediction_history, name='prediction_history'),
    
    # Chatbot
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('chatbot/api/', views.chatbot_api, name='chatbot_api'),
    path('chatbot/reset/', views.reset_chatbot, name='reset_chatbot'),
]
