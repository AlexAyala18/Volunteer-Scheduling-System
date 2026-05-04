# backend/routes/event_routes.py

import sys
from flask import Blueprint, request, jsonify
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from backend.models.mongo import get_event_collection

# Blueprint for event-related API routes
event_bp = Blueprint("event_routes", __name__)

@event_bp.route("/api/events", methods=["GET"])
def list_events():
    try:
        # Log the attempt to fetch events
        print("Attempting to fetch events from MongoDB...")
        
        # Get the events collection
        events_collection = get_event_collection()
        
        # Fetch all events, excluding the MongoDB _id field
        events = list(events_collection.find({}, {"_id": 0}))
        
        # Log success
        print(f"Successfully fetched {len(events)} events")
        
        return jsonify(events), 200
    except ConnectionFailure as e:
        # Log the error
        print(f"ERROR in list_events - MongoDB connection failure: {str(e)}", file=sys.stderr)
        return jsonify({
            "error": "Database connection error",
            "message": "Could not connect to MongoDB. Please check your connection.",
            "details": str(e)
        }), 500
    except ServerSelectionTimeoutError as e:
        # Log the error
        print(f"ERROR in list_events - MongoDB server selection timeout: {str(e)}", file=sys.stderr)
        return jsonify({
            "error": "Database connection timeout",
            "message": "Could not connect to MongoDB server. Please check if MongoDB is running.",
            "details": str(e)
        }), 500
    except Exception as e:
        # Log the error
        print(f"ERROR in list_events: {str(e)}", file=sys.stderr)
        return jsonify({"error": f"Failed to fetch events: {str(e)}"}), 500

@event_bp.route("/api/events", methods=["POST"])
def create_event():
    try:
        # Log the attempt to create an event
        print("Attempting to create a new event...")
        
        # Parse the request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        # Check for required fields
        required = ["event_id", "event_name", "form_config"]
        for key in required:
            if key not in data:
                return jsonify({"error": f"Missing required field: {key}"}), 400

        # Validate event_id format (no spaces, special characters limited)
        event_id = data["event_id"]
        if not event_id.isalnum():
            return jsonify({"error": "Event ID must contain only letters and numbers"}), 400

        # Prevent duplicate event IDs
        if get_event_collection().find_one({"event_id": event_id}):
            return jsonify({"error": f"Event with ID '{event_id}' already exists"}), 400

        # Log the event data (excluding form_config for brevity)
        print(f"Creating event: {event_id} - {data['event_name']}")
        
        # Insert the event into the database
        result = get_event_collection().insert_one(data)
        
        # Check if insertion was successful
        if result.acknowledged:
            print(f"Event '{event_id}' created successfully!")
            return jsonify({"message": "Event created successfully!", "event_id": event_id}), 201
        else:
            return jsonify({"error": "Failed to create event: Database operation not acknowledged"}), 500
            
    except ConnectionFailure as e:
        # Log the error
        print(f"ERROR in create_event - MongoDB connection failure: {str(e)}", file=sys.stderr)
        return jsonify({
            "error": "Database connection error",
            "message": "Could not connect to MongoDB. Please check your connection.",
            "details": str(e)
        }), 500
    except ServerSelectionTimeoutError as e:
        # Log the error
        print(f"ERROR in create_event - MongoDB server selection timeout: {str(e)}", file=sys.stderr)
        return jsonify({
            "error": "Database connection timeout",
            "message": "Could not connect to MongoDB server. Please check if MongoDB is running.",
            "details": str(e)
        }), 500
    except Exception as e:
        # Log the error
        print(f"ERROR in create_event: {str(e)}", file=sys.stderr)
        return jsonify({"error": f"Failed to create event: {str(e)}"}), 500

@event_bp.route("/api/events/<event_id>", methods=["GET"])
def get_event(event_id):
    try:
        event = get_event_collection().find_one({"event_id": event_id}, {"_id": 0})
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify(event), 200
    except ConnectionFailure as e:
        # Log the error
        print(f"ERROR in get_event - MongoDB connection failure: {str(e)}", file=sys.stderr)
        return jsonify({
            "error": "Database connection error",
            "message": "Could not connect to MongoDB. Please check your connection.",
            "details": str(e)
        }), 500
    except ServerSelectionTimeoutError as e:
        # Log the error
        print(f"ERROR in get_event - MongoDB server selection timeout: {str(e)}", file=sys.stderr)
        return jsonify({
            "error": "Database connection timeout",
            "message": "Could not connect to MongoDB server. Please check if MongoDB is running.",
            "details": str(e)
        }), 500
    except Exception as e:
        # Log the error
        print(f"ERROR in get_event: {str(e)}", file=sys.stderr)
        return jsonify({"error": f"Failed to fetch event: {str(e)}"}), 500

@event_bp.route("/api/events/<event_id>", methods=["PUT"])
def update_event(event_id):
    try:
        # Parse the request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        # Check if the event exists
        event = get_event_collection().find_one({"event_id": event_id})
        if not event:
            return jsonify({"error": "Event not found"}), 404
            
        # Check for required fields
        required = ["event_name", "form_config"]
        for key in required:
            if key not in data:
                return jsonify({"error": f"Missing required field: {key}"}), 400
                
        # If event_id is being changed, check that the new ID doesn't already exist
        new_event_id = data.get("event_id")
        if new_event_id and new_event_id != event_id:
            # Validate event_id format
            if not new_event_id.isalnum():
                return jsonify({"error": "Event ID must contain only letters and numbers"}), 400
                
            # Check if the new ID already exists
            if get_event_collection().find_one({"event_id": new_event_id}):
                return jsonify({"error": f"Event with ID '{new_event_id}' already exists"}), 400
                
            # Update the event with the new ID
            result = get_event_collection().replace_one({"event_id": event_id}, data)
            
            # Rename the volunteer collection if it exists
            from backend.models.mongo import get_volunteer_collection, get_db
            db = get_db()
            old_collection_name = f"volunteers_{event_id}"
            new_collection_name = f"volunteers_{new_event_id}"
            
            if old_collection_name in db.list_collection_names():
                db[old_collection_name].rename(new_collection_name)
                
            event_id = new_event_id  # Update event_id for the response
        else:
            # Keep the same event_id, just update the other fields
            result = get_event_collection().replace_one({"event_id": event_id}, data)
        
        if result.modified_count == 0:
            return jsonify({"error": "Failed to update event"}), 500
            
        return jsonify({
            "message": f"Event '{event_id}' updated successfully",
            "event_id": event_id
        }), 200
    except ConnectionFailure as e:
        # Log the error
        print(f"ERROR in update_event - MongoDB connection failure: {str(e)}", file=sys.stderr)
        return jsonify({
            "error": "Database connection error",
            "message": "Could not connect to MongoDB. Please check your connection.",
            "details": str(e)
        }), 500
    except ServerSelectionTimeoutError as e:
        # Log the error
        print(f"ERROR in update_event - MongoDB server selection timeout: {str(e)}", file=sys.stderr)
        return jsonify({
            "error": "Database connection timeout",
            "message": "Could not connect to MongoDB server. Please check if MongoDB is running.",
            "details": str(e)
        }), 500
    except Exception as e:
        # Log the error
        print(f"ERROR in update_event: {str(e)}", file=sys.stderr)
        return jsonify({"error": f"Failed to update event: {str(e)}"}), 500

@event_bp.route("/api/events/<event_id>", methods=["DELETE"])
def delete_event(event_id):
    try:
        # Check if the event exists
        event = get_event_collection().find_one({"event_id": event_id})
        if not event:
            return jsonify({"error": "Event not found"}), 404
            
        # Delete the event
        result = get_event_collection().delete_one({"event_id": event_id})
        
        if result.deleted_count == 0:
            return jsonify({"error": "Failed to delete event"}), 500
            
        # Also delete all volunteer data associated with this event
        from backend.models.mongo import get_volunteer_collection
        volunteer_collection = get_volunteer_collection(event_id)
        volunteer_collection.drop()
        
        return jsonify({"message": f"Event '{event_id}' and all associated volunteer data deleted successfully"}), 200
    except ConnectionFailure as e:
        # Log the error
        print(f"ERROR in get_event - MongoDB connection failure: {str(e)}", file=sys.stderr)
        return jsonify({
            "error": "Database connection error",
            "message": "Could not connect to MongoDB. Please check your connection.",
            "details": str(e)
        }), 500
    except ServerSelectionTimeoutError as e:
        # Log the error
        print(f"ERROR in get_event - MongoDB server selection timeout: {str(e)}", file=sys.stderr)
        return jsonify({
            "error": "Database connection timeout",
            "message": "Could not connect to MongoDB server. Please check if MongoDB is running.",
            "details": str(e)
        }), 500
    except Exception as e:
        # Log the error
        print(f"ERROR in get_event: {str(e)}", file=sys.stderr)
        return jsonify({"error": f"Failed to fetch event: {str(e)}"}), 500
