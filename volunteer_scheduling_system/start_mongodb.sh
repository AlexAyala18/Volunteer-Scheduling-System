#!/bin/bash
# Simple script to start MongoDB on macOS or Linux
# For Windows users, please start MongoDB as a service or use the MongoDB Compass application

echo "Starting MongoDB..."

# Check if mongod is in the PATH
if command -v mongod &> /dev/null; then
    # Check if MongoDB is already running
    if pgrep mongod > /dev/null; then
        echo "MongoDB is already running."
    else
        # Try to create data directory if it doesn't exist
        mkdir -p ~/data/db 2>/dev/null

        # Start MongoDB with the data directory
        echo "Starting MongoDB server..."
        mongod --dbpath ~/data/db
    fi
else
    echo "MongoDB (mongod) not found in PATH."
    echo "Please make sure MongoDB is installed correctly."
    echo ""
    echo "Installation guides:"
    echo "- macOS: brew install mongodb-community"
    echo "  or visit: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/"
    echo "- Linux (Ubuntu): sudo apt-get install -y mongodb"
    echo "  or visit: https://docs.mongodb.com/manual/administration/install-on-linux/"
    echo ""
    echo "After installing, try running this script again."
    exit 1
fi
