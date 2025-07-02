@echo off
echo 🚀 Setting up DataInsight AI for Windows...
echo.

echo 📦 Setting up Backend...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error: Python not found or failed to create virtual environment
        echo Please install Python 3.8+ and try again
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error installing Python dependencies
    pause
    exit /b 1
)

echo ✅ Backend setup complete!
echo.

cd ..

echo 📦 Setting up Frontend...
cd frontend

echo Installing Node.js dependencies...
npm install
if errorlevel 1 (
    echo ❌ Error: Node.js not found or failed to install dependencies
    echo Please install Node.js 16+ and try again
    pause
    exit /b 1
)

echo ✅ Frontend setup complete!
echo.

cd ..

echo 🎉 Setup complete! To start the application:
echo.
echo 1. Backend: Run "start_backend.bat"
echo 2. Frontend: Run "start_frontend.bat" (in a new terminal)
echo.
echo The application will be available at:
echo - Backend API: http://localhost:8000
echo - Frontend UI: http://localhost:3000
echo.

pause