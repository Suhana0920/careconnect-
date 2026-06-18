#!/bin/bash

# CareConnect+ Django Server Startup Script

echo ""
echo "===================================="
echo "CareConnect+ Login System"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

echo "[1/4] Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[2/4] Running migrations..."
python3 manage.py migrate

if [ $? -ne 0 ]; then
    echo "WARNING: Migration may have failed"
fi

echo "[3/4] Starting Django development server..."
echo ""
echo "===================================="
echo "Server is running at:"
echo "  http://127.0.0.1:8000/"
echo ""
echo "Admin panel:"
echo "  http://127.0.0.1:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"
echo "===================================="
echo ""

python3 manage.py runserver
