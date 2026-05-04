import os
import sys
import traceback
import secrets
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, OperationFailure

from backend.models.mongo import init_mongo
from backend.routes.form_routes import form_bp
from backend.routes.event_routes import event_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.volunteer_routes import volunteer_bp
from backend.config import config

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Print MongoDB URI (with password masked for security)
    mongo_uri = config.MONGO_URI
    masked_uri = mongo_uri
    if "@" in mongo_uri and ":" in mongo_uri:
        # Mask the password in the URI for logging
        parts = mongo_uri.split("@")
        credentials = parts[0].split(":")
        if len(credentials) > 2:
            masked_uri = f"{credentials[0]}:****@{parts[1]}"
    
    print(f"Using MongoDB URI: {masked_uri}")

    # Dynamically resolve template/static folder paths
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, "../frontend/templates")
    static_dir = os.path.join(base_dir, "../frontend/static")

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    # Set a secret key for session management
    # In production, this should be set in environment variables
    app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(16))
    
    # Configure Flask-Mail
    app.config['MAIL_SERVER'] = os.environ.get('SMTP_SERVER')
    app.config['MAIL_PORT'] = int(os.environ.get('SMTP_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.environ.get('SMTP_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('SMTP_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Initialize Flask-Mail
    mail = Mail(app)
    
    # Make mail available to other modules
    app.mail = mail
    
    CORS(app)
    
    # Set up error handlers
    @app.errorhandler(500)
    def handle_server_error(error):
        """Handle 500 Internal Server Error"""
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server.",
            "details": str(error)
        }), 500
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 Not Found Error"""
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found on the server."
        }), 404
    
    # Custom route for MongoDB connection errors
    @app.route("/db-error")
    def db_error():
        """Display MongoDB connection error page"""
        return render_template("error.html", 
                              error_title="Database Connection Error",
                              error_message="Could not connect to MongoDB. Please check your connection.")

    # Try to initialize MongoDB connection
    mongodb_connected = False
    try:
        init_mongo(app)
        mongodb_connected = True
        print(f"MongoDB connection established successfully!")
    except (ConnectionFailure, ServerSelectionTimeoutError, OperationFailure) as e:
        print(f"ERROR: Failed to connect to MongoDB: {e}", file=sys.stderr)
        print("\nPossible solutions:", file=sys.stderr)
        print("1. Check if your MongoDB Atlas cluster is running", file=sys.stderr)
        print("2. Verify your IP address is whitelisted in MongoDB Atlas", file=sys.stderr)
        print("3. Confirm the username and password in the connection string are correct", file=sys.stderr)
        print("4. Make sure your network allows connections to MongoDB Atlas", file=sys.stderr)
        
        # Create a mock MongoDB implementation for development
        print("\nUsing in-memory database for development...", file=sys.stderr)
        
        # Mock the MongoDB collections
        class MockDB:
            def __init__(self):
                self.events = []
                self.volunteers = {}
                
            def add_event(self, event):
                self.events.append(event)
                
            def get_events(self):
                return self.events
                
            def get_event(self, event_id):
                for event in self.events:
                    if event.get('event_id') == event_id:
                        return event
                return None
                
            def add_volunteer(self, event_id, volunteer):
                if event_id not in self.volunteers:
                    self.volunteers[event_id] = []
                self.volunteers[event_id].append(volunteer)
                
            def get_volunteers(self, event_id):
                return self.volunteers.get(event_id, [])
        
        # Create a global mock database
        mock_db = MockDB()
        
        # Override the MongoDB routes to use the mock database
        @app.route('/api/events', methods=['GET'])
        def mock_list_events():
            return jsonify(mock_db.get_events()), 200
            
        @app.route('/api/events', methods=['POST'])
        def mock_create_event():
            data = request.get_json()
            
            # Validate required fields
            required = ["event_id", "event_name", "form_config"]
            for key in required:
                if key not in data:
                    return jsonify({"error": f"Missing required field: {key}"}), 400
                    
            # Check for duplicate event IDs
            if mock_db.get_event(data['event_id']):
                return jsonify({"error": f"Event with ID '{data['event_id']}' already exists"}), 400
                
            # Add the event to the mock database
            mock_db.add_event(data)
            
            return jsonify({
                "message": "Event created successfully!",
                "event_id": data['event_id'],
                "note": "Using in-memory database (MongoDB connection failed)"
            }), 201
            
        @app.route('/api/events/<event_id>', methods=['GET'])
        def mock_get_event(event_id):
            event = mock_db.get_event(event_id)
            if not event:
                return jsonify({"error": "Event not found"}), 404
            return jsonify(event), 200
            
        @app.route('/api/volunteers/<event_id>', methods=['POST'])
        def mock_submit_volunteer(event_id):
            data = request.get_json()
            
            # Check if the event exists
            event = mock_db.get_event(event_id)
            if not event:
                return jsonify({"error": "Event not found"}), 404
                
            # Add the volunteer to the mock database
            mock_db.add_volunteer(event_id, data)
            
            return jsonify({
                "message": "Volunteer submission successful!",
                "note": "Using in-memory database (MongoDB connection failed)"
            }), 201
            
        @app.route('/api/volunteers/<event_id>', methods=['GET'])
        def mock_list_volunteers(event_id):
            # Check if the event exists
            event = mock_db.get_event(event_id)
            if not event:
                return jsonify({"error": "Event not found"}), 404
                
            return jsonify(mock_db.get_volunteers(event_id)), 200
        
        # Add a specific error handler for MongoDB-related API requests
        @app.errorhandler(500)
        def handle_mongodb_error(error):
            return jsonify({
                "error": "Database connection error",
                "message": "Could not connect to MongoDB. Using in-memory database for development.",
                "details": str(e)
            }), 500
    except Exception as e:
        print(f"ERROR: Unexpected error initializing MongoDB: {e}", file=sys.stderr)
        traceback.print_exc()

    # Register blueprints for all routes
    app.register_blueprint(form_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(volunteer_bp)
    
    # Root route redirects to admin login
    @app.route("/")
    def index():
        return redirect(url_for("admin_routes.login"))

    # Add a health check endpoint
    @app.route("/health")
    def health_check():
        """Health check endpoint"""
        status = "ok" if mongodb_connected else "degraded"
        return jsonify({
            "status": status,
            "mongodb": "connected" if mongodb_connected else "disconnected"
        })

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
