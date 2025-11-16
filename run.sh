#!/bin/bash

# University Rankings Scraper - Run Script

echo "=================================="
echo "  University Rankings Scraper"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip is not installed"
    echo "Please install pip"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "backend/venv" ]; then
    echo "Creating virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
    cd ..
else
    echo "Using existing virtual environment..."
    cd backend
    source venv/bin/activate
    cd ..
fi

# Start backend server
echo ""
echo "Starting backend server..."
echo "Backend will be available at: http://localhost:5001"
echo ""
echo "To access the frontend:"
echo "  Open frontend/index.html in your browser"
echo "  OR run: cd frontend && python3 -m http.server 8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd backend
python app.py
