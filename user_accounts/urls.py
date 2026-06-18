from django.urls import path
from . import views

urlpatterns = [
    # ── Authentication ────────────────────────────────────────────────────────
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards (ROLE-BASED)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard_view, name='doctor_dashboard'),
    
    # Admin Portal
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout_view, name='admin_logout'),
    path('admin/patient/<int:patient_id>/', views.admin_patient_detail_view, name='admin_patient_detail'),
    path('admin/doctors/', views.admin_all_doctors_view, name='admin_all_doctors'),
    path('admin/appointments/', views.admin_all_appointments_view, name='admin_all_appointments'),
    path('rbac-demo/', views.admin_rbac_demo_view, name='rbac_demo'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    
    # Doctors & Appointments
    path('doctors/', views.doctors_list_view, name='doctors_list'),
    path('book-appointment/', views.book_appointment_view, name='book_appointment'),
    path('book_appointment/<int:doctor_id>/', views.book_appointment_view, name='book_appointment_with_doctor'),
    
    # Medical Records & History
    path('patient/medical-records/', views.patient_medical_records_view, name='patient_medical_records'),
    path('patient/update-medical-record/', views.update_medical_record_view, name='update_medical_record'),
    
    # AI Chatbot
     path('chat/', views.chat_ai_view, name='chat_ai'),
    
    # Other
    path('notifications/', views.notifications_view, name='notifications'),
]