#!/bin/bash
# Setup script for the Volunteer Scheduling System
# This script creates a virtual environment and installs dependencies

echo "Setting up Volunteer Scheduling System..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please check your Python installation."
        exit 1
    fi
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    exit 1
fi

echo ""
echo "Setup completed successfully!"
echo ""
echo "To start the application:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start MongoDB (if using local installation):"
echo "   ./start_mongodb.sh"
echo ""
echo "3. Run the application:"
echo "   python run.py"
echo ""
echo "For more information, see README.md"
