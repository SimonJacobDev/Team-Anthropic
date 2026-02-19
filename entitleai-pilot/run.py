#!/usr/bin/env python
import os
import sys
import subprocess
import webbrowser
from time import sleep

def main():
    print("🚀 Starting EntitleAI-Pilot...")
    print("=" * 50)
    
    # Change to backend directory
    os.chdir('backend')
    
    # Check if database exists
    if not os.path.exists('entitleai.db'):
        print("📦 Initializing database with 1000 households...")
        subprocess.run([sys.executable, 'init_db.py'])
    
    # Open browser
    print("🌐 Opening browser in 3 seconds...")
    webbrowser.open('http://localhost:5000')
    webbrowser.open_new_tab('http://localhost:5000/dashboard')
    
    # Run Flask app
    print("🚀 Starting Flask server...")
    print("📊 Main app: http://localhost:5000")
    print("📈 Dashboard: http://localhost:5000/dashboard")
    print("=" * 50)
    print("Press Ctrl+C to stop")
    
    subprocess.run([sys.executable, 'app.py'])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        sys.exit(0)
