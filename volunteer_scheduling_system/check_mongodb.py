#!/usr/bin/env python3
"""
MongoDB Connection Check Script

This script checks if MongoDB is running and accessible.
It's useful for diagnosing connection issues before starting the application.
"""

import sys
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, OperationFailure
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variables
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/volunteer_db")

def mask_uri(uri):
    """Mask the password in the URI for secure logging."""
    if "@" in uri and ":" in uri:
        # Split the URI into parts
        parts = uri.split("@")
        if len(parts) == 2:
            credentials = parts[0].split(":")
            if len(credentials) > 2:
                # Format: mongodb+srv://username:password@cluster
                return f"{credentials[0]}:****@{parts[1]}"
    return uri

def check_mongodb_connection():
    """Check if MongoDB is running and accessible."""
    print(f"Checking MongoDB connection to: {mask_uri(mongo_uri)}")
    
    try:
        # Create a MongoDB client with a short timeout
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Force a connection to verify it works
        client.admin.command('ping')
        
        # Get database name from URI
        db_name = mongo_uri.split('/')[-1].split('?')[0]
        
        print(f"✅ Successfully connected to MongoDB!")
        print(f"   Database: {db_name}")
        
        # Check if we can access the events collection
        try:
            events_count = client[db_name].events.count_documents({})
            print(f"   Found {events_count} events in the database")
        except Exception as e:
            print(f"   Note: Could not count events: {e}")
        
        return True
    
    except ConnectionFailure as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("\nPossible solutions:")
        print("1. Make sure MongoDB is installed and running")
        print("2. Check your connection string in the .env file")
        return False
    
    except ServerSelectionTimeoutError as e:
        print(f"❌ MongoDB server selection timeout: {e}")
        
        if "mongodb+srv" in mongo_uri:
            print("\nPossible solutions for MongoDB Atlas:")
            print("1. Check if your MongoDB Atlas cluster is running")
            print("2. Verify your IP address is whitelisted in MongoDB Atlas")
            print("3. Confirm the username and password in the connection string are correct")
            print("4. Make sure your network allows connections to MongoDB Atlas")
        else:
            print("\nPossible solutions for local MongoDB:")
            print("1. Make sure MongoDB is running and accessible")
            print("2. Check if the MongoDB port is open (default: 27017)")
            print("3. Verify your network configuration allows connections to MongoDB")
        
        return False
    
    except OperationFailure as e:
        print(f"❌ MongoDB operation failure: {e}")
        
        if "Authentication failed" in str(e):
            print("\nAuthentication failed. Possible solutions:")
            print("1. Check if the username and password in the connection string are correct")
            print("2. Verify that the user has the necessary permissions")
        else:
            print("\nPossible solutions:")
            print("1. Check if you have the necessary permissions")
            print("2. Verify your connection string is correct")
        
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("MongoDB Connection Checker")
    print("==========================")
    
    if check_mongodb_connection():
        print("\nYour MongoDB connection is working correctly!")
        print("You should be able to run the application without connection issues.")
        sys.exit(0)  # Success
    else:
        print("\nFailed to connect to MongoDB.")
        print("Please fix the connection issues before running the application.")
        
        if "mongodb+srv" in mongo_uri:
            print("\nFor MongoDB Atlas issues:")
            print("1. Log in to your MongoDB Atlas account")
            print("2. Check if your cluster is running")
            print("3. Go to Network Access and add your current IP address")
            print("4. Verify the connection string in your .env file")
        
        sys.exit(1)  # Failure
