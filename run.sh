#!/bin/bash
set -e

echo "Setting up AI BI Streamlit Reports..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete! Starting Streamlit app..."
echo ""

# Run the app
streamlit run app.py
