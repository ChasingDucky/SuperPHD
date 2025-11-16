@echo off
REM University Rankings Scraper - Run Script (Windows)

echo ==================================
echo   University Rankings Scraper
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist "backend\venv" (
    echo Creating virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
    cd ..
) else (
    echo Using existing virtual environment...
    cd backend
    call venv\Scripts\activate.bat
    cd ..
)

REM Start backend server
echo.
echo Starting backend server...
echo Backend will be available at: http://localhost:5001
echo.
echo To access the frontend:
echo   Open frontend\index.html in your browser
echo   OR run: cd frontend ^&^& python -m http.server 8000
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python app.py
