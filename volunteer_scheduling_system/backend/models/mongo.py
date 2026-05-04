# backend/models/mongo.py

import sys
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from backend.config import config

mongo = PyMongo()

def init_mongo(app):
    """
    Initialize MongoDB connection with improved error handling.
    
    Args:
        app: Flask application instance
        
    Raises:
        ConnectionFailure: If unable to connect to MongoDB
        ServerSelectionTimeoutError: If MongoDB server selection times out
    """
    try:
        # Set the MongoDB URI from config
        app.config["MONGO_URI"] = config.MONGO_URI
        
        # Initialize PyMongo with the Flask app
        mongo.init_app(app)
        
        # Test the connection by accessing the database
        # This will raise an exception if the connection fails
        mongo.db.command('ping')
        
        print(f"MongoDB connection successful. Database: {mongo.db.name}")
        
        # Create the events collection if it doesn't exist
        if "events" not in mongo.db.list_collection_names():
            mongo.db.create_collection("events")
            print("Created 'events' collection")
            
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        if "localhost" in config.MONGO_URI or "127.0.0.1" in config.MONGO_URI:
            print(f"ERROR: Failed to connect to local MongoDB: {e}", file=sys.stderr)
            print("\nPossible solutions:", file=sys.stderr)
            print("1. Make sure MongoDB is installed and running locally", file=sys.stderr)
            print("2. Run 'mongod' in a terminal to start MongoDB", file=sys.stderr)
            print("3. Check if MongoDB is running on the default port (27017)", file=sys.stderr)
        else:
            print(f"ERROR: Failed to connect to MongoDB Atlas: {e}", file=sys.stderr)
            print("\nPossible solutions:", file=sys.stderr)
            print("1. Check if your MongoDB Atlas cluster is running", file=sys.stderr)
            print("2. Verify your IP address is whitelisted in MongoDB Atlas", file=sys.stderr)
            print("3. Confirm the username and password in the connection string are correct", file=sys.stderr)
        raise

def get_event_collection():
    """
    Get the events collection from MongoDB.
    
    Returns:
        pymongo.collection.Collection: The events collection
        
    Raises:
        Exception: If MongoDB is not initialized
    """
    if mongo.db is None:
        raise Exception("MongoDB is not initialized. Check your connection.")
    return mongo.db.events

def get_volunteer_collection(event_id):
    """
    Get the volunteers collection for a specific event.
    
    Args:
        event_id (str): The event ID
        
    Returns:
        pymongo.collection.Collection: The volunteers collection for the event
        
    Raises:
        Exception: If MongoDB is not initialized
    """
    if mongo.db is None:
        raise Exception("MongoDB is not initialized. Check your connection.")
    return mongo.db[f"volunteers_{event_id}"]

def get_db():
    """
    Get the MongoDB database instance.
    
    Returns:
        pymongo.database.Database: The MongoDB database instance
        
    Raises:
        Exception: If MongoDB is not initialized
    """
    if mongo.db is None:
        raise Exception("MongoDB is not initialized. Check your connection.")
    return mongo.db
