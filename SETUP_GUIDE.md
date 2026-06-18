# CareConnect+ Django Setup Guide

## Quick Start (Windows)

### Step 1: Install Python
1. Download Python from https://www.python.org/downloads/
2. Install with **"Add Python to PATH"** checked
3. Verify installation:
   ```powershell
   python --version
   ```

### Step 2: Setup & Run
1. Open PowerShell in the `careconnect+` folder
2. Double-click `run_server.bat` OR run:
   ```powershell
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

### Step 3: Access the Application
- **Login Page:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## Setup (Linux/Mac)

### Step 1: Install Python & Pip
```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# macOS
brew install python3
```

### Step 2: Setup & Run
```bash
# Make script executable
chmod +x run_server.sh

# Run the server
./run_server.sh
```

Or manually:
```bash
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

---

## Project Structure

```
careconnect+/
├── careconnect/              # Main Django project
│   ├── __init__.py
│   ├── settings.py           # Django configuration
│   ├── urls.py               # URL routing
│   ├── wsgi.py               # WSGI application
│   └── asgi.py               # ASGI application
├── login/                    # Login app
│   ├── __init__.py
│   ├── admin.py              # Admin configuration
│   ├── apps.py               # App config
│   ├── models.py             # Database models
│   ├── views.py              # View logic
│   └── urls.py               # App URLs
├── templates/
│   └── login.html            # Login page template
├── static/                   # Static files (CSS, JS, images)
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── run_server.bat            # Windows startup script
├── run_server.sh             # Linux/Mac startup script
└── README_DJANGO.md          # Project documentation
```

---

## Features

✅ **Modern UI**
- Responsive design with Tailwind CSS
- Smooth animations and transitions
- Real-time clock and statistics

✅ **Login System**
- Email and password authentication
- Password strength meter
- Role selection (Patient, Doctor, Admin)
- CSRF protection

✅ **Dashboard Preview**
- Live user counts
- Recent activity feed
- Patient testimonials
- Medical specialties carousel

✅ **API Endpoints**
- `GET /` - Login page
- `POST /api/login/` - Authentication API

---

## Configuration

### Change Secret Key (For Production)
Edit `careconnect/settings.py`:
```python
SECRET_KEY = 'your-new-secret-key-here'
```

### Change Debug Mode (For Production)
Edit `careconnect/settings.py`:
```python
DEBUG = False
```

### Add Custom Domain
Edit `careconnect/settings.py`:
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

---

## Database

- **Type:** SQLite (default)
- **Location:** `db.sqlite3`
- **Reset:** Delete `db.sqlite3` and run `python manage.py migrate`

---

## Admin Panel

Create admin account:
```bash
python manage.py createsuperuser
```

Access at: http://127.0.0.1:8000/admin/

---

## Dependencies

- Django 4.2.0 - Web framework
- Django REST Framework 3.14.0 - API framework
- django-cors-headers 4.0.0 - CORS support
- Daphne 4.0.0 - ASGI server

---

## Troubleshooting

### "Port 8000 already in use"
```bash
python manage.py runserver 8001
```

### "No module named 'django'"
```bash
pip install -r requirements.txt
```

### "ImportError: No module named 'login'"
```bash
python manage.py migrate
```

### Static files not loading
```bash
python manage.py collectstatic
```

---

## Next Steps

1. **Add Real Authentication:**
   - Use Django's built-in User model
   - Add password hashing
   - Implement JWT tokens

2. **Add Database:**
   - Create User, Doctor, Patient models
   - Setup relationships
   - Add migrations

3. **Add Frontend:**
   - Create dashboard views
   - Add navigation
   - Implement user sessions

4. **Deploy:**
   - Use Gunicorn + Nginx
   - Deploy to Heroku, AWS, or DigitalOcean
   - Setup SSL certificate

---

## Support

For issues or questions, check:
- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Tailwind CSS: https://tailwindcss.com/

---

**Happy coding! 🎉**
