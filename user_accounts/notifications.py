from django.core.mail import send_mail
from django.conf import settings

def send_appointment_confirmation_email(appointment):
    """Send appointment confirmation email to patient"""
    subject = f'Appointment Confirmed - Dr. {appointment.doctor.name}'
    
    message = f"""
Dear {appointment.patient.get_full_name() or appointment.patient.username},

Your appointment has been confirmed!

Details:
- Doctor: Dr. {appointment.doctor.name}
- Specialty: {appointment.doctor.get_specialty_display()}
- Date: {appointment.appointment_date.strftime('%B %d, %Y')}
- Time: {appointment.get_appointment_time_display()}
- Consultation Fee: ₹{appointment.doctor.consultation_fee}

Reason: {appointment.reason}

Please arrive 15 minutes before your scheduled time.

Thank you for choosing CareConnect+!

Best regards,
CareConnect+ Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.patient.email],
            fail_silently=False,
        )
        appointment.email_sent = True
        appointment.save()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False