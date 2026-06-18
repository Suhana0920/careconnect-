from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    UserProfile, Doctor, Appointment, 
    MedicalRecord, Prescription, VitalSigns, LabReport, AIChatMessage
)   

# Customize User Admin to show profiles
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['role', 'phone', 'address', 'date_of_birth']

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'profile__role']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    def get_role(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.role
        return 'No Profile'
    get_role.short_description = 'Role'
    get_role.admin_order_field = 'profile__role'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'date_of_birth']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['user']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'experience', 'consultation_fee', 'total_appointments']
    list_filter = ['specialty', 'experience']
    search_fields = ['name', 'qualification', 'specialty']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'specialty', 'qualification', 'user')
        }),
        ('Professional Details', {
            'fields': ('experience', 'consultation_fee', 'about')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
    )
    
    def total_appointments(self, obj):
        return obj.appointments.count()
    total_appointments.short_description = 'Total Appointments'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient_name', 'doctor_name', 'appointment_date', 'appointment_time', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'created_at']
    search_fields = ['patient__username', 'patient__email', 'doctor__name', 'reason']
    list_editable = ['status']
    date_hierarchy = 'appointment_date'
    ordering = ['-appointment_date', '-appointment_time']
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'appointment_date', 'appointment_time')
        }),
        ('Additional Information', {
            'fields': ('reason', 'status')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def patient_name(self, obj):
        return obj.patient.get_full_name() or obj.patient.username
    patient_name.short_description = 'Patient'
    patient_name.admin_order_field = 'patient__username'
    
    def doctor_name(self, obj):
        return f"Dr. {obj.doctor.name}"
    doctor_name.short_description = 'Doctor'
    doctor_name.admin_order_field = 'doctor__name'
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} appointments marked as confirmed.')
    mark_as_confirmed.short_description = 'Mark selected as Confirmed'
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} appointments marked as completed.')
    mark_as_completed.short_description = 'Mark selected as Completed'
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} appointments marked as cancelled.')
    mark_as_cancelled.short_description = 'Mark selected as Cancelled'


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'blood_group', 'height', 'weight', 'allergies_preview', 'updated_at']
    list_filter = ['blood_group', 'updated_at']
    search_fields = ['patient__username', 'patient__email', 'allergies', 'chronic_conditions']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient',)
        }),
        ('Physical Details', {
            'fields': ('blood_group', 'height', 'weight')
        }),
        ('Medical Information', {
            'fields': ('allergies', 'chronic_conditions', 'current_medications')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def allergies_preview(self, obj):
        return obj.allergies[:30] + '...' if obj.allergies and len(obj.allergies) > 30 else obj.allergies or 'None'
    allergies_preview.short_description = 'Allergies'


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'diagnosis_preview', 'created_at', 'follow_up_date']
    list_filter = ['created_at', 'follow_up_date', 'doctor']
    search_fields = ['patient__username', 'doctor__name', 'diagnosis', 'medicines']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def diagnosis_preview(self, obj):
        return obj.diagnosis[:40] + '...' if len(obj.diagnosis) > 40 else obj.diagnosis
    diagnosis_preview.short_description = 'Diagnosis'


@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ['patient', 'blood_pressure', 'heart_rate', 'temperature', 'oxygen_saturation', 'recorded_at']
    list_filter = ['recorded_at']
    search_fields = ['patient__username']
    date_hierarchy = 'recorded_at'
    ordering = ['-recorded_at']


@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = ['patient', 'test_name', 'test_date', 'result_preview', 'created_at']
    list_filter = ['test_date', 'created_at']
    search_fields = ['patient__username', 'test_name', 'result']
    date_hierarchy = 'test_date'
    ordering = ['-test_date']
    
    def result_preview(self, obj):
        return obj.result[:50] + '...' if len(obj.result) > 50 else obj.result
    result_preview.short_description = 'Result'


@admin.register(AIChatMessage)
class AIChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'sender_type', 'message_preview', 'timestamp']
    list_filter = ['sender_type', 'timestamp']
    search_fields = ['user__username', 'message']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
    
    fieldsets = (
        ('Message Information', {
            'fields': ('user', 'sender_type', 'message')
        }),
        ('Metadata', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )
    
    def message_preview(self, obj):
        return obj.message[:80] + '...' if len(obj.message) > 80 else obj.message
    message_preview.short_description = 'Message'


# Customize Admin Site
admin.site.site_header = "CareConnect+ Administration"
admin.site.site_title = "CareConnect+ Admin"
admin.site.index_title = "Welcome to CareConnect+ Admin Panel"