#!/bin/bash

echo "🚀 Starting EntitleAI-Pilot..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Navigate to backend directory
cd backend

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Initialize database if needed
if [ ! -f "entitleai.db" ]; then
    echo "🗄️  Initializing database with 1000 households..."
    python3 init_db.py
fi

# Start the server
echo "🌐 Starting Flask server on http://localhost:5000"
echo "📊 Dashboard available at http://localhost:5000/dashboard"
echo "Press Ctrl+C to stop"

python3 app.py