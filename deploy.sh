#!/bin/bash

# Auracelle Bach - Quick Deployment Script
# This script sets up and runs Auracelle Bach locally

set -e  # Exit on error

echo "🎼 Auracelle Bach - Quick Deployment"
echo "===================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip -q
echo "✅ Pip upgraded"

# Install dependencies
echo ""
echo "📚 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt -q
echo "✅ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found"
    read -p "Would you like to create one from .env.example? (y/n): " create_env
    if [ "$create_env" = "y" ] || [ "$create_env" = "Y" ]; then
        cp .env.example .env
        echo "✅ Created .env file - please edit it with your API keys"
        echo "   Run: nano .env"
    fi
fi

# Verify installation
echo ""
echo "🧪 Verifying installation..."
python3 -c "import streamlit; import pandas; import numpy; import plotly; import networkx; print('✅ All core modules imported successfully')"

echo ""
echo "🚀 Starting Auracelle Bach..."
echo "===================================="
echo ""
echo "The application will open in your default browser."
echo "If it doesn't open automatically, visit: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run Streamlit
streamlit run app.py
