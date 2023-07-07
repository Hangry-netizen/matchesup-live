#!/bin/bash
set -e

# Navigate to the application directory
cd /start.py

# Activate the virtual environment (if applicable)
source venv/bin/activate

# Start the Flask app server
python app.py
