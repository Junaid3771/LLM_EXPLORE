#!/bin/bash

echo "🚀 Starting DataInsight AI Backend..."

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo "🎯 Starting FastAPI server on http://localhost:8000"
echo "📊 Ready to analyze your data!"
python main.py