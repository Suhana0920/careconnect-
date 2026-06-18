# CareConnect+ Backend Setup Guide

## 🚀 Backend Implementation Complete!

Your Django backend for the CareConnect+ login system is now set up. Follow these steps to get it running:

### 1. **Install Dependencies**

Make sure you have Django and required packages installed:

```bash
pip install django djangorestframework django-cors-headers pillow
```

Or install from requirements:
```bash
pip install -r requirements.txt
```

### 2. **Run Database Migrations**

Navigate to your project directory and run:

```bash
python manage.py makemigrations login
python manage.py migrate
```

This will create the following database tables:
- **UserProfile** - Stores user information (patient, doctor, or admin)
- **DoctorProfile** - Stores doctor-specific information
- **LoginAttempt** - Logs all login attempts for security tracking

### 3. **Create a Superuser (Admin Account)**

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. You can use:
- Email: `admin@example.com`
- Password: (choose a secure password)

### 4. **Start the Django Server**

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

### 5. **Access the Dashboard**

- **Login Page**: http://localhost:8000/login/
- **Admin Panel**: http://localhost:8000/admin/
- **Dashboard** (after login): http://localhost:8000/login/dashboard/

### 📋 **Feature Overview**

#### User Models Created:

1. **UserProfile**
   - Linked to Django's User model
   - Stores: user_type (patient/doctor/admin), phone, age, bio, profile picture
   - Tracks: is_verified, created_at, updated_at

2. **DoctorProfile**
   - Extended doctor information
   - Stores: license number, specialty, hospital, experience years, rating
   - Features: consultation fee, availability status, review count

3. **LoginAttempt**
   - Security logging
   - Tracks: email, user type, success/failure, timestamp, IP address

#### API Endpoints:

All endpoints require CSRF token from cookies:

- **POST** `/login/api/login/` - User login
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "user_type": "patient"
  }
  ```

- **POST** `/login/api/register/` - User registration
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "confirm_password": "password123",
    "age": 25,
    "user_type": "patient"
  }
  ```

- **GET** `/login/api/logout/` - User logout

- **GET** `/login/api/profile/` - Get current user's profile (requires login)

### 🧪 **Testing the System**

#### Test Registration:
1. Go to http://localhost:8000/login/
2. Click "Register" tab
3. Fill in the form with:
   - Name: John Doe
   - Email: john@example.com
   - Age: 25
   - Password: TestPass123
   - Confirm Password: TestPass123
4. Click "Create My Account"

#### Test Login:
1. Follow the "Sign In" tab
2. Use the email and password you just created
3. Click "Sign In to Account"
4. You'll be redirected to the dashboard

### 📊 **Admin Panel Features**

Access admin panel at: http://localhost:8000/admin/

**Features:**
- User profile management
- Doctor profile management with specialty filtering
- Login attempt tracking and monitoring
- User verification status management
- Doctor availability toggling

### 🔒 **Security Features Implemented**

✓ CSRF protection enabled
✓ Password validation (minimum 6 characters)
✓ Email uniqueness validation
✓ IP address logging for login attempts
✓ User type verification
✓ Password hashing using Django's built-in system
✓ CORS configuration for API access

### 🔧 **Next Steps**

1. **Email Verification**: Add email verification for new accounts
2. **Password Reset**: Implement forgot password functionality
3. **Social Login**: Add Google/Microsoft OAuth integration
4. **Two-Factor Authentication**: Enhance security with 2FA
5. **Doctor Verification**: Add admin approval for doctor registration
6. **Appointment System**: Build appointment scheduling
7. **Database**: Migrate from SQLite to PostgreSQL for production

### 📁 **File Structure**

```
login/
├── admin.py          # Admin panel configuration (UPDATED)
├── apps.py           
├── forms.py          # Form validation (NEW)
├── models.py         # Database models (UPDATED)
├── urls.py           # API endpoints (UPDATED)
├── views.py          # View functions & API (UPDATED)
└── migrations/       # Database migrations
```

### 🛠️ **Troubleshooting**

**Issue**: ModuleNotFoundError
- **Solution**: Make sure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Column doesn't exist errors
- **Solution**: Run migrations: `python manage.py migrate`

**Issue**: CSRF token missing
- **Solution**: The login.html automatically extracts CSRF token from cookies

**Issue**: 404 error on API endpoints
- **Solution**: Make sure Django server is running and check URL routes in urls.py

### 📞 **Support**

For issues or questions:
1. Check Django Debug Toolbar (enable DEBUG=True in settings.py)
2. Check terminal for error messages
3. Review Django logs for API errors

---

**Last Updated**: February 7, 2026
**Version**: 1.0
