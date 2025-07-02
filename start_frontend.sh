#!/bin/bash

echo "🎨 Starting DataInsight AI Frontend..."

# Navigate to frontend directory
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Start the development server
echo "🎯 Starting React development server on http://localhost:3000"
echo "🌟 Beautiful UI loading..."
npm start