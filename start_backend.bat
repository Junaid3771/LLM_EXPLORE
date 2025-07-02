@echo off
echo 🚀 Starting DataInsight AI Backend...

REM Navigate to backend directory
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Start the server
echo 🎯 Starting FastAPI server on http://localhost:8000
echo 📊 Ready to analyze your data!
python main.py

pause