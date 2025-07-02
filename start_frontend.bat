@echo off
echo 🎨 Starting DataInsight AI Frontend...

REM Navigate to frontend directory
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing Node.js dependencies...
    npm install
    if errorlevel 1 (
        echo ❌ Error: Failed to install dependencies
        echo Please ensure Node.js 16+ is installed
        pause
        exit /b 1
    )
)

REM Start the development server
echo 🎯 Starting React development server on http://localhost:3000
echo 🌟 Beautiful UI loading...
echo.
echo Press Ctrl+C to stop the server
npm start

pause