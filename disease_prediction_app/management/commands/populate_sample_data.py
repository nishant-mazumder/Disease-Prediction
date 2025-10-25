from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from disease_prediction_app.models import Doctor, UserProfile
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample doctors with Indian locations and INR fees
        doctors_data = [
            {
                'name': 'Dr. Rajesh Kumar',
                'specialization': 'cardiology',
                'location': 'Delhi, India',
                'phone_number': '+91-9876543210',
                'email': 'rajesh.kumar@medpredict.com',
                'rating': 4.8,
                'fees': Decimal('1500.00'),
                'experience_years': 15,
                'bio': 'Dr. Rajesh Kumar is a board-certified cardiologist with over 15 years of experience in treating heart conditions. He specializes in interventional cardiology and has performed over 2000 successful procedures.'
            },
            {
                'name': 'Dr. Priya Sharma',
                'specialization': 'endocrinology',
                'location': 'Mumbai, India',
                'phone_number': '+91-9876543211',
                'email': 'priya.sharma@medpredict.com',
                'rating': 4.9,
                'fees': Decimal('1200.00'),
                'experience_years': 12,
                'bio': 'Dr. Priya Sharma specializes in diabetes management and endocrine disorders. She has helped thousands of patients manage their diabetes effectively.'
            },
            {
                'name': 'Dr. Amit Patel',
                'specialization': 'neurology',
                'location': 'Bangalore, India',
                'phone_number': '+91-9876543212',
                'email': 'amit.patel@medpredict.com',
                'rating': 4.7,
                'fees': Decimal('1800.00'),
                'experience_years': 18,
                'bio': 'Dr. Amit Patel is a leading neurologist specializing in movement disorders and Parkinson\'s disease. He has extensive experience in treating neurological conditions.'
            },
            {
                'name': 'Dr. Sunita Reddy',
                'specialization': 'general',
                'location': 'Hyderabad, India',
                'phone_number': '+91-9876543213',
                'email': 'sunita.reddy@medpredict.com',
                'rating': 4.6,
                'fees': Decimal('800.00'),
                'experience_years': 20,
                'bio': 'Dr. Sunita Reddy provides comprehensive primary care services. She has been serving the community for over 20 years with dedication and compassion.'
            },
            {
                'name': 'Dr. Vikram Singh',
                'specialization': 'pediatrics',
                'location': 'Chennai, India',
                'phone_number': '+91-9876543214',
                'email': 'vikram.singh@medpredict.com',
                'rating': 4.9,
                'fees': Decimal('1000.00'),
                'experience_years': 14,
                'bio': 'Dr. Vikram Singh is a pediatrician with expertise in child health and development. He is known for his gentle approach with children.'
            },
            {
                'name': 'Dr. Anjali Gupta',
                'specialization': 'dermatology',
                'location': 'Pune, India',
                'phone_number': '+91-9876543215',
                'email': 'anjali.gupta@medpredict.com',
                'rating': 4.5,
                'fees': Decimal('1300.00'),
                'experience_years': 16,
                'bio': 'Dr. Anjali Gupta specializes in skin conditions and cosmetic dermatology. She has helped many patients achieve healthy, beautiful skin.'
            },
            {
                'name': 'Dr. Ravi Verma',
                'specialization': 'orthopedics',
                'location': 'Kolkata, India',
                'phone_number': '+91-9876543216',
                'email': 'ravi.verma@medpredict.com',
                'rating': 4.8,
                'fees': Decimal('1600.00'),
                'experience_years': 13,
                'bio': 'Dr. Ravi Verma is an orthopedic surgeon specializing in sports medicine and joint replacement surgeries.'
            },
            {
                'name': 'Dr. Meera Joshi',
                'specialization': 'cardiology',
                'location': 'Ahmedabad, India',
                'phone_number': '+91-9876543217',
                'email': 'meera.joshi@medpredict.com',
                'rating': 4.7,
                'fees': Decimal('1400.00'),
                'experience_years': 17,
                'bio': 'Dr. Meera Joshi is a cardiologist with expertise in interventional procedures and cardiac rehabilitation.'
            },
            {
                'name': 'Dr. Suresh Kumar',
                'specialization': 'endocrinology',
                'location': 'Jaipur, India',
                'phone_number': '+91-9876543218',
                'email': 'suresh.kumar@medpredict.com',
                'rating': 4.6,
                'fees': Decimal('1100.00'),
                'experience_years': 11,
                'bio': 'Dr. Suresh Kumar focuses on diabetes care and metabolic disorders. He has a special interest in gestational diabetes.'
            },
            {
                'name': 'Dr. Kavita Nair',
                'specialization': 'neurology',
                'location': 'Kochi, India',
                'phone_number': '+91-9876543219',
                'email': 'kavita.nair@medpredict.com',
                'rating': 4.9,
                'fees': Decimal('1700.00'),
                'experience_years': 19,
                'bio': 'Dr. Kavita Nair is a neurologist specializing in epilepsy and seizure disorders. She has extensive experience in treating complex neurological cases.'
            },
            {
                'name': 'Dr. Arjun Mehta',
                'specialization': 'cardiology',
                'location': 'Chandigarh, India',
                'phone_number': '+91-9876543220',
                'email': 'arjun.mehta@medpredict.com',
                'rating': 4.8,
                'fees': Decimal('1350.00'),
                'experience_years': 16,
                'bio': 'Dr. Arjun Mehta is a renowned cardiologist with expertise in preventive cardiology and heart failure management.'
            },
            {
                'name': 'Dr. Neha Agarwal',
                'specialization': 'pediatrics',
                'location': 'Indore, India',
                'phone_number': '+91-9876543221',
                'email': 'neha.agarwal@medpredict.com',
                'rating': 4.7,
                'fees': Decimal('900.00'),
                'experience_years': 10,
                'bio': 'Dr. Neha Agarwal is a dedicated pediatrician with expertise in neonatal care and child development.'
            },
            {
                'name': 'Dr. Manoj Tiwari',
                'specialization': 'orthopedics',
                'location': 'Lucknow, India',
                'phone_number': '+91-9876543222',
                'email': 'manoj.tiwari@medpredict.com',
                'rating': 4.6,
                'fees': Decimal('1250.00'),
                'experience_years': 14,
                'bio': 'Dr. Manoj Tiwari specializes in trauma surgery and sports injuries. He has treated numerous athletes and sports professionals.'
            },
            {
                'name': 'Dr. Deepika Shah',
                'specialization': 'dermatology',
                'location': 'Surat, India',
                'phone_number': '+91-9876543223',
                'email': 'deepika.shah@medpredict.com',
                'rating': 4.8,
                'fees': Decimal('1150.00'),
                'experience_years': 12,
                'bio': 'Dr. Deepika Shah is a dermatologist with expertise in medical and cosmetic dermatology. She has a special interest in skin cancer detection.'
            },
            {
                'name': 'Dr. Rohit Malhotra',
                'specialization': 'general',
                'location': 'Nagpur, India',
                'phone_number': '+91-9876543224',
                'email': 'rohit.malhotra@medpredict.com',
                'rating': 4.5,
                'fees': Decimal('750.00'),
                'experience_years': 18,
                'bio': 'Dr. Rohit Malhotra provides comprehensive primary care services with a focus on preventive medicine and health promotion.'
            }
        ]
        
        for doctor_data in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                email=doctor_data['email'],
                defaults=doctor_data
            )
            if created:
                self.stdout.write(f'Created doctor: {doctor.name}')
        
        # Create a sample user if it doesn't exist
        if not User.objects.filter(username='demo_user').exists():
            user = User.objects.create_user(
                username='demo_user',
                email='demo@medpredict.com',
                password='demo123',
                first_name='Demo',
                last_name='User'
            )
            UserProfile.objects.create(user=user)
            self.stdout.write('Created demo user: demo_user (password: demo123)')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample data!')
        )
