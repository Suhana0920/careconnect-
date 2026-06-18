@echo off
REM CareConnect+ Django Server Startup Script

echo.
echo ====================================
echo CareConnect+ Login System
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [2/4] Running migrations...
python manage.py migrate

if errorlevel 1 (
    echo WARNING: Migration may have failed
)

echo [3/4] Creating superuser (optional)...
echo Press Ctrl+C to skip and proceed to running the server

python manage.py createsuperuser --noinput 2>nul || echo Superuser creation skipped

echo.
echo [4/4] Starting Django development server...
echo.
echo ====================================
echo Server is running at:
echo   http://127.0.0.1:8000/
echo.
echo Admin panel:
echo   http://127.0.0.1:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.

python manage.py runserver

pause
