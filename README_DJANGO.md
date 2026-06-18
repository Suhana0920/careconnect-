# CareConnect+ Django Project

A modern healthcare platform login system built with Django, Tailwind CSS, and dynamic JavaScript.

## Project Structure

```
careconnect+/
├── careconnect/           # Main Django project
│   ├── settings.py       # Django settings
│   ├── urls.py           # URL configuration
│   ├── wsgi.py           # WSGI application
│   └── asgi.py           # ASGI application
├── login/                # Login app
│   ├── views.py          # View logic
│   ├── urls.py           # App URLs
│   └── apps.py           # App configuration
├── templates/            # HTML templates
│   └── login.html        # Login page template
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations (if needed):**
   ```bash
   python manage.py migrate
   ```

3. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

4. **Access the application:**
   - Open your browser and go to `http://127.0.0.1:8000/`

## Features

- ✅ **Real-time Clock** - Displays current time and date
- ✅ **Live Statistics** - Shows doctors, patients, and appointments online
- ✅ **Animated UI** - Smooth transitions and animations
- ✅ **Password Strength Meter** - Real-time password validation
- ✅ **Role Selection** - Choose between Patient, Doctor, or Admin
- ✅ **Responsive Design** - Works on all devices
- ✅ **CSRF Protection** - Django security middleware enabled
- ✅ **API Endpoint** - `/api/login/` for handling authentication

## API Endpoints

### POST `/api/login/`
Handle user login requests.

**Request:**
```json
{
    "email": "user@example.com",
    "password": "password123",
    "userType": "patient"
}
```

**Response (Success):**
```json
{
    "success": true,
    "message": "Login successful!",
    "user_type": "patient",
    "email": "user@example.com",
    "timestamp": "2024-02-06T10:30:00"
}
```

## Customization

- **Change site name:** Edit `SITE_NAME` in `settings.py`
- **Update colors:** Modify Tailwind classes in `templates/login.html`
- **Add real authentication:** Extend the `api_login` view in `login/views.py`

## Requirements

- Python 3.8+
- Django 4.2.0
- Django REST Framework 3.14.0
- django-cors-headers 4.0.0
- Daphne 4.0.0 (optional, for async support)

## License

MIT License - Feel free to use this project for your own healthcare platform!
