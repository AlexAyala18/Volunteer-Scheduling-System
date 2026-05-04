#!/usr/bin/env python3
"""
Run script for the Volunteer Scheduling System.
This script starts the Flask application with the correct configuration.
"""

import os
from backend.app import create_app

def main():
    """
    Main function to run the application.
    """
    print("Starting Volunteer Scheduling System...")
    
    # Check if MongoDB connection is configured
    if not os.getenv("MONGO_URI"):
        print("\nWARNING: MONGO_URI environment variable not found.")
        print("The application will attempt to connect to a local MongoDB instance.")
        print("If you encounter connection issues, please set up MongoDB and update the .env file.")
        print("See README.md for instructions on setting up MongoDB.\n")
    
    # Create and run the Flask application
    app = create_app()
    
    # Get port from command line or use default
    port = int(os.environ.get("PORT", 5000))    # replace the sys.argv line
    
    print(f"\nServer starting on http://localhost:{port}")
    print(f"Admin Dashboard: http://localhost:{port}/admin")
    print(f"Volunteer Events: http://localhost:{port}/volunteer/events")
    print("\nPress Ctrl+C to stop the server")
    
    # Run the application
    app.run(debug=False, host="0.0.0.0", port=port)   # replace the debug=True line


if __name__ == "__main__":
    main()
