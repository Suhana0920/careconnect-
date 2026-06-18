from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Doctor, Appointment, AIChatMessage
from django.db.models import Q


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'profile'):
                if user.profile.role == 'admin':
                    return redirect('/admin/')
                elif user.profile.role == 'doctor':
                    return redirect('doctor_dashboard')
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            return render(request, 'login.html', {'register_error': 'Passwords do not match'})
        if User.objects.filter(username=email).exists():
            return render(request, 'login.html', {'register_error': 'Email already registered'})
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name.split()[0] if name else ''
        )
        login(request, user)
        return redirect('dashboard')
    return redirect('login')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by('-appointment_date')[:5]
    
    context = {
        'appointments': appointments,
        'user_appointments_count': Appointment.objects.filter(patient=request.user).count(),
    }
    
    return render(request, 'dashboard.html', context)

def doctor_dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
        return redirect('dashboard')
    try:
        doctor_profile = request.user.doctor_profile
        appointments = Appointment.objects.filter(doctor=doctor_profile)
    except:
        appointments = []
    return render(request, 'doctor_dashboard.html', {'appointments': appointments})

def admin_dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return redirect('dashboard')
    
    from django.contrib.auth.models import User
    
    total_patients = User.objects.filter(profile__role='patient').count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    
    recent_appointments = Appointment.objects.all().order_by('-created_at')[:10]
    all_doctors = Doctor.objects.all()
    all_patients = User.objects.filter(profile__role='patient')
    
    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'recent_appointments': recent_appointments,
        'all_doctors': all_doctors,
        'all_patients': all_patients,
    }
    
    return render(request, 'admin_dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        if current_password and new_password:
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                login(request, user)
                return render(request, 'profile.html', {'success': 'Profile and password updated!'})
            else:
                return render(request, 'profile.html', {'error': 'Current password is incorrect'})
        return render(request, 'profile.html', {'success': 'Profile updated!'})
    return render(request, 'profile.html')

def doctors_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    doctors = Doctor.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        doctors = doctors.filter(name__icontains=search_query)
    specialty_filter = request.GET.get('specialty', '')
    if specialty_filter:
        doctors = doctors.filter(specialty=specialty_filter)
    specialties = Doctor.SPECIALTY_CHOICES
    return render(request, 'doctors_list.html', {
        'doctors': doctors,
        'specialties': specialties,
        'search_query': search_query,
        'specialty_filter': specialty_filter,
    })

def book_appointment_view(request, doctor_id=None):
    if not request.user.is_authenticated:
        return redirect('login')

    doctors = Doctor.objects.all()

    if request.method == 'POST':
        selected_doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason', '')

        if not selected_doctor_id:
            return render(request, 'book_appointment.html', {
                'error': 'Please select a doctor',
                'doctors': doctors,
                'time_slots': Appointment.TIME_SLOTS,
            })

        try:
            doctor = Doctor.objects.get(id=selected_doctor_id)
        except Doctor.DoesNotExist:
            return render(request, 'book_appointment.html', {
                'error': 'Doctor not found',
                'doctors': doctors,
                'time_slots': Appointment.TIME_SLOTS,
            })

        existing = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists()

        if existing:
            return render(request, 'book_appointment.html', {
                'error': 'This time slot is already booked. Please choose another.',
                'doctors': doctors,
                'time_slots': Appointment.TIME_SLOTS,
            })

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            status='pending'
        )

        return redirect('dashboard')  # ✅ Redirect to dashboard after booking!

    return render(request, 'book_appointment.html', {
        'doctors': doctors,
        'time_slots': Appointment.TIME_SLOTS,
    })

def notifications_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('dashboard')
# ── AI Chat ────────────────────────────────────────────────────────────────────

def chat_ai_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    chat_messages = AIChatMessage.objects.filter(user=request.user).order_by('timestamp')

    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        if user_message:
            AIChatMessage.objects.create(
                user=request.user,
                message=user_message,
                sender_type='user'
            )
            ai_reply = generate_ai_reply(user_message, request.user)
            AIChatMessage.objects.create(
                user=request.user,
                message=ai_reply,
                sender_type='ai'
            )
            return redirect('chat_ai')

    context = {
        'user': request.user,
        'messages': chat_messages,
    }
    return render(request, 'chat_ai.html', context)


def generate_ai_reply(message, user):
    message_lower = message.lower()

    # Greetings
    if any(w in message_lower for w in ['hello', 'hi', 'hey', 'good morning', 'good evening', 'good afternoon']):
        patient_name = user.first_name or user.username
        return f"Hello {patient_name}! 👋 I'm your AI Health Assistant. I can help you with health questions, symptoms, appointments and more. What can I help you with today?"

    # Appointment booking
    elif any(w in message_lower for w in ['book', 'appointment', 'schedule', 'slot', 'reserve']):
        return "To book an appointment: Go to 'Book Appointment' from your dashboard → Select a doctor → Choose date and time slot → Confirm. Would you like help with anything else?"

    # Depression / mental health
    elif any(w in message_lower for w in ['depression', 'depressed', 'sad', 'lonely', 'hopeless', 'anxious', 'anxiety', 'stress', 'stressed', 'mental', 'mood', 'unhappy']):
        return ("💙 I understand you're going through a tough time. Here are some tips to help with depression:\n"
                "• Talk to someone you trust — a friend, family member or counsellor\n"
                "• Exercise daily — even a 20-minute walk helps boost mood\n"
                "• Maintain a regular sleep schedule\n"
                "• Avoid alcohol and isolation\n"
                "• Practice mindfulness or meditation\n"
                "• Eat a balanced diet\n"
                "Please consider booking an appointment with our Psychiatrist for professional support. You are not alone! 💙")

    # Fever
    elif any(w in message_lower for w in ['fever', 'temperature', 'hot body', 'chills']):
        return ("🌡️ For fever:\n"
                "• Rest and stay hydrated — drink plenty of water\n"
                "• Take paracetamol if temperature is above 38°C\n"
                "• Use a cool damp cloth on forehead\n"
                "• Avoid heavy clothing\n"
                "⚠️ See a doctor if fever goes above 39.5°C or lasts more than 3 days.")

    # Cold / cough
    elif any(w in message_lower for w in ['cold', 'cough', 'sneeze', 'runny nose', 'blocked nose', 'sore throat']):
        return ("🤧 For cold and cough:\n"
                "• Drink warm fluids — honey-ginger tea, warm water with lemon\n"
                "• Steam inhalation helps with congestion\n"
                "• Gargle with warm salt water for sore throat\n"
                "• Rest well and avoid cold drinks\n"
                "Most colds resolve in 7-10 days. See a doctor if symptoms worsen.")

    # Headache / migraine
    elif any(w in message_lower for w in ['headache', 'head pain', 'migraine', 'head ache']):
        return ("🤕 For headaches:\n"
                "• Rest in a quiet, dark room\n"
                "• Stay hydrated — dehydration causes headaches\n"
                "• Apply cold or warm compress on forehead\n"
                "• Take paracetamol for pain relief\n"
                "• For migraines: avoid bright lights, loud sounds and stress\n"
                "⚠️ See a neurologist if headaches are frequent or very severe.")

    # Stomach / digestion
    elif any(w in message_lower for w in ['stomach', 'abdomen', 'nausea', 'vomit', 'diarrhea', 'loose motion', 'constipation', 'indigestion', 'bloating', 'gas']):
        return ("🫄 For stomach issues:\n"
                "• Stay hydrated — drink ORS or electrolyte drinks\n"
                "• Eat light foods: rice, bananas, toast, boiled potatoes\n"
                "• Avoid spicy, oily or heavy foods\n"
                "• Take probiotics to restore gut health\n"
                "⚠️ See a doctor if pain is severe or symptoms persist over 48 hours.")

    # Chest pain / heart
    elif any(w in message_lower for w in ['chest', 'heart', 'chest pain', 'palpitation', 'heartbeat']):
        return "⚠️ IMPORTANT: Chest pain or irregular heartbeat can be serious. Please consult a doctor immediately or call emergency services (112) if the pain is severe. Do not ignore these symptoms!"

    # Breathing
    elif any(w in message_lower for w in ['breath', 'breathing', 'shortness', 'asthma', 'inhaler']):
        return ("😮‍💨 For breathing issues:\n"
                "• Sit upright and stay calm\n"
                "• Use your inhaler if prescribed\n"
                "• Practice pursed lip breathing\n"
                "⚠️ If breathing difficulty is sudden or severe, call emergency services (112) immediately!")

    # Back pain / joint pain
    elif any(w in message_lower for w in ['back pain', 'back ache', 'joint', 'knee', 'shoulder', 'neck pain', 'spine']):
        return ("🦴 For back/joint pain:\n"
                "• Apply ice pack for first 48 hours, then warm compress\n"
                "• Rest but avoid complete bed rest\n"
                "• Do gentle stretching exercises\n"
                "• Maintain good posture while sitting\n"
                "• Take pain relief medication if needed\n"
                "Consider booking with our Orthopaedic specialist for persistent pain.")

    # Diabetes / blood sugar
    elif any(w in message_lower for w in ['diabetes', 'blood sugar', 'insulin', 'glucose', 'sugar level']):
        return ("🩺 For diabetes management:\n"
                "• Monitor blood sugar levels regularly\n"
                "• Follow a low-sugar, high-fibre diet\n"
                "• Exercise at least 30 minutes daily\n"
                "• Take medications as prescribed\n"
                "• Avoid skipping meals\n"
                "• Stay hydrated\n"
                "Please book regular checkups with our General Physician or Cardiologist.")

    # Blood pressure
    elif any(w in message_lower for w in ['blood pressure', 'bp', 'hypertension', 'high bp', 'low bp']):
        return ("❤️ For blood pressure:\n"
                "• Reduce salt intake in your diet\n"
                "• Exercise regularly — walking, swimming\n"
                "• Maintain healthy weight\n"
                "• Avoid smoking and alcohol\n"
                "• Manage stress through meditation\n"
                "• Take medications as prescribed\n"
                "Book with our Cardiologist for regular monitoring.")

    # Sleep problems
    elif any(w in message_lower for w in ['sleep', 'insomnia', 'cant sleep', 'sleepless', 'tired', 'fatigue', 'exhausted']):
        return ("😴 For better sleep:\n"
                "• Maintain a fixed sleep schedule\n"
                "• Avoid screens 1 hour before bed\n"
                "• Keep your room dark and cool\n"
                "• Avoid caffeine after 3 PM\n"
                "• Try relaxation techniques — deep breathing, meditation\n"
                "• Avoid heavy meals before bedtime")

    # Diet / nutrition
    elif any(w in message_lower for w in ['diet', 'nutrition', 'eat', 'food', 'weight', 'obesity', 'fat', 'calories']):
        return ("🥗 For a healthy diet:\n"
                "• Eat plenty of fruits and vegetables\n"
                "• Choose whole grains over refined carbs\n"
                "• Drink 8 glasses of water daily\n"
                "• Limit sugar, salt and processed foods\n"
                "• Eat smaller portions more frequently\n"
                "• Include protein in every meal")

    # Exercise / fitness
    elif any(w in message_lower for w in ['exercise', 'workout', 'fitness', 'gym', 'yoga', 'walk']):
        return ("💪 Exercise recommendations:\n"
                "• Aim for at least 30 minutes of moderate exercise daily\n"
                "• Walking, cycling, swimming are great options\n"
                "• Yoga helps with flexibility and mental health\n"
                "• Stretch before and after workouts\n"
                "• Start slowly and gradually increase intensity\n"
                "• Stay hydrated during exercise")

    # Medical records
    elif any(w in message_lower for w in ['record', 'prescription', 'history', 'report', 'lab', 'vital']):
        return "You can view your complete medical history, prescriptions, vital signs and lab reports in the Medical Records section. Click 'Medical Records' from your dashboard or sidebar."

    # Emergency
    elif any(w in message_lower for w in ['emergency', 'urgent', 'critical', 'dying', 'unconscious']):
        return "🚨 EMERGENCY: Please call 112 immediately or go to the nearest hospital! Do not wait — your health is the top priority!"

    # Thanks
    elif any(w in message_lower for w in ['thank', 'thanks', 'great', 'helpful', 'good', 'awesome']):
        return "You're welcome! 😊 Stay healthy and feel free to ask me anything anytime!"

    # Symptoms general
    elif any(w in message_lower for w in ['symptom', 'symptoms', 'watch', 'warning', 'sign']):
        return ("⚠️ Common symptoms to watch for:\n"
                "• Persistent fever above 38°C for more than 3 days\n"
                "• Sudden chest pain or difficulty breathing\n"
                "• Severe headache or dizziness\n"
                "• Unexplained weight loss\n"
                "• Persistent cough for more than 2 weeks\n"
                "• Unusual fatigue or weakness\n"
                "• Changes in vision or hearing\n"
                "If you experience any of these, please book an appointment with a doctor!")

    # Default
    else:
        return (f"I understand you asked about '{message}'. "
                "I can help with: symptoms, fever, cold, headache, depression, diabetes, blood pressure, sleep, diet, exercise, appointments and more. "
                "Could you please be more specific so I can give you better advice? 😊")
    
# ==================== MEDICAL RECORDS ====================

def patient_medical_records_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        from .models import MedicalRecord, Prescription, VitalSigns, LabReport
        medical_record = request.user.medical_record
    except:
        from .models import MedicalRecord
        medical_record = MedicalRecord.objects.create(patient=request.user)
    
    try:
        from .models import Prescription, VitalSigns, LabReport
        prescriptions = Prescription.objects.filter(patient=request.user).order_by('-created_at')[:10]
        vital_signs = VitalSigns.objects.filter(patient=request.user).order_by('-recorded_at')[:10]
        lab_reports = LabReport.objects.filter(patient=request.user).order_by('-test_date')[:10]
    except:
        prescriptions = []
        vital_signs = []
        lab_reports = []
    
    context = {
        'user': request.user,
        'medical_record': medical_record,
        'prescriptions': prescriptions,
        'vital_signs': vital_signs,
        'lab_reports': lab_reports,
    }
    return render(request, 'patient/medical_records.html', context)

def update_medical_record_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        from .models import MedicalRecord
        medical_record = request.user.medical_record
    except:
        from .models import MedicalRecord
        medical_record = MedicalRecord.objects.create(patient=request.user)
    
    if request.method == 'POST':
        medical_record.blood_group = request.POST.get('blood_group', '')
        medical_record.height = request.POST.get('height', None)
        medical_record.weight = request.POST.get('weight', None)
        medical_record.allergies = request.POST.get('allergies', '')
        medical_record.chronic_conditions = request.POST.get('chronic_conditions', '')
        medical_record.current_medications = request.POST.get('current_medications', '')
        medical_record.emergency_contact_name = request.POST.get('emergency_contact_name', '')
        medical_record.emergency_contact_phone = request.POST.get('emergency_contact_phone', '')
        medical_record.emergency_contact_relation = request.POST.get('emergency_contact_relation', '')
        medical_record.save()
        
        return redirect('patient_medical_records')
    
    context = {
        'user': request.user,
        'medical_record': medical_record,
    }
    return render(request, 'patient/update_medical_record.html', context)
# ==================== ADMIN VIEWS ====================

def admin_login_view(request):
    """Separate login page for admin"""
    if request.user.is_authenticated:
        if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'admin'):
            return redirect('admin_dashboard')
        else:
            logout(request)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin'):
                login(request, user)
                return redirect('admin_dashboard')
            else:
                return render(request, 'admin_login.html', {'error': 'Access Denied: Admin privileges required'})
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'admin_login.html')


def admin_dashboard_view(request):
    """Admin dashboard showing all patients"""
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'admin')):
        return redirect('login')
    
    # Get all patients
    patients = User.objects.filter(profile__role='patient').order_by('-date_joined')
    
    # Statistics
    total_doctors = Doctor.objects.count()
    total_patients = patients.count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    
    context = {
        'user': request.user,
        'patients': patients,
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
    }
    
    return render(request, 'admin_custom/dashboard.html', context)


def admin_patient_detail_view(request, patient_id):
    """View individual patient details"""
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'admin')):
        return redirect('login')
    
    from .models import MedicalRecord, Prescription
    
    patient = User.objects.get(id=patient_id)
    
    try:
        medical_record = patient.medical_record
    except:
        medical_record = None
    
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    prescriptions = Prescription.objects.filter(patient=patient).order_by('-created_at')
    
    context = {
        'user': request.user,
        'patient': patient,
        'medical_record': medical_record,
        'appointments': appointments,
        'prescriptions': prescriptions,
    }
    
    return render(request, 'admin_custom/patient_detail.html', context)


def admin_logout_view(request):
    """Admin logout"""
    logout(request)
    return redirect('admin_login')


def admin_all_doctors_view(request):
    """View all doctors"""
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'admin')):
        return redirect('login')
    
    doctors = Doctor.objects.all().order_by('name')
    
    context = {
        'user': request.user,
        'doctors': doctors,
    }
    
    return render(request, 'admin_custom/all_doctors.html', context)


def admin_all_appointments_view(request):
    """View all appointments"""
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'admin')):
        return redirect('login')
    
    appointments = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    context = {
        'user': request.user,
        'appointments': appointments,
        'status_filter': status_filter,
    }
    
    return render(request, 'admin_custom/all_appointments.html', context)


def admin_rbac_demo_view(request):
    """RBAC demonstration page"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get counts for each role
    admin_count = User.objects.filter(is_superuser=True).count() + User.objects.filter(profile__role='admin').count()
    doctor_count = User.objects.filter(profile__role='doctor').count()
    patient_count = User.objects.filter(profile__role='patient').count()
    
    context = {
        'user': request.user,
        'admin_count': admin_count,
        'doctor_count': doctor_count,
        'patient_count': patient_count,
    }
    
    return render(request, 'rbac_demo.html', context)