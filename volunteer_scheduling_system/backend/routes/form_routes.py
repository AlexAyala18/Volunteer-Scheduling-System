# backend/routes/form_routes.py

import datetime
import logging
from flask import Blueprint, request, jsonify, Response
from backend.models.mongo import get_volunteer_collection, get_db
from backend.utils.excel_generator import export_event_to_excel
from backend.utils.shift_config import get_shift_labels, format_shifts_summary
from backend.utils.email_service import email_service
from backend.utils.calendar_generator import generate_ical_file, generate_google_calendar_url

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

form_bp = Blueprint("form_routes", __name__)

@form_bp.route("/api/submit/<event_id>", methods=["POST"])
def submit_form(event_id):
    try:
        data = request.get_json()
        data["event_id"] = event_id

        # Use the validation function from form_config_loader
        from backend.utils.form_config_loader import validate_form_submission
        is_valid, error_message = validate_form_submission(data)
        
        if not is_valid:
            return jsonify({"error": error_message}), 400

        # Defaults for optional fields
        data["organization"] = data.get("organization", "")
        data["certifications"] = data.get("certifications", [])
        data["shifts"] = data.get("shifts", {})
        data["emergency_contact_name"] = data.get("emergency_contact_name", "")
        data["emergency_contact_phone"] = data.get("emergency_contact_phone", "")
        data["submit_date"] = datetime.datetime.now().isoformat()

        # Save volunteer data to database
        get_volunteer_collection(event_id).insert_one(data)

        # Get event details
        events_collection = get_db().events
        event_data = events_collection.find_one({"event_id": event_id})
        
        # Build shift summary using centralized configuration with dynamic shift times
        summary = format_shifts_summary(data["shifts"], event_data)
        
        # Send confirmation email
        email_sent = False
        try:
            # Event data is already fetched above
            
            if event_data and data.get("email"):
                # Extract language preference (default to English if not provided)
                language = data.get("language_preference", "en")
                
                # Send confirmation email with language preference
                email_sent = email_service.send_volunteer_confirmation(data, event_data, language)
                if email_sent:
                    logger.info(f"Confirmation email sent to {data['email']} for event {event_id} in {language}")
                else:
                    logger.warning(f"Failed to send confirmation email to {data['email']} for event {event_id}")
            else:
                logger.warning(f"Could not send confirmation email: event data or volunteer email missing")
        except Exception as email_error:
            # Log the error but don't fail the submission
            logger.error(f"Error sending confirmation email: {str(email_error)}")
        
        return jsonify({
            "message": "Submitted!", 
            "shiftSummary": summary,
            "emailSent": email_sent
        }), 200

    except Exception as e:
        logger.error(f"Error in form submission: {str(e)}")
        return jsonify({"error": str(e)}), 500

@form_bp.route("/api/volunteers/<event_id>", methods=["GET"])
def get_volunteers(event_id):
    try:
        volunteers = list(get_volunteer_collection(event_id).find({}, {"_id": 0}))
        return jsonify(volunteers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@form_bp.route("/api/volunteer/<event_id>/<email>", methods=["DELETE"])
def delete_volunteer(event_id, email):
    try:
        result = get_volunteer_collection(event_id).delete_one({"email": email})
        if result.deleted_count == 1:
            return jsonify({"message": "Deleted"}), 200
        return jsonify({"error": "Volunteer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from backend.utils.excel_generator import export_event_to_excel

@form_bp.route("/api/export-excel/<event_id>", methods=["GET"])
def export_excel(event_id):
    try:
        return export_event_to_excel(event_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@form_bp.route("/api/calendar/<event_id>/<email>", methods=["GET"])
def get_calendar(event_id, email):
    """
    Generate and serve an iCalendar file for a volunteer's shifts.
    
    Args:
        event_id (str): The ID of the event
        email (str): The email of the volunteer
        
    Returns:
        Response: iCalendar file as a downloadable attachment or webcal protocol
    """
    try:
        # Get event data
        events_collection = get_db().events
        event_data = events_collection.find_one({"event_id": event_id})
        
        if not event_data:
            return jsonify({"error": "Event not found"}), 404
        
        # Get volunteer data
        volunteer_collection = get_volunteer_collection(event_id)
        volunteer_data = volunteer_collection.find_one({"email": email})
        
        if not volunteer_data:
            return jsonify({"error": "Volunteer not found"}), 404
        
        # Extract shift information
        shifts = volunteer_data.get("shifts", {})
        
        # Convert shifts to a format suitable for calendar generation
        shift_details = []
        
        for shift_key, selected in shifts.items():
            if not selected:
                continue
                
            # Parse shift key (e.g., "monday_shift1")
            parts = shift_key.split('_')
            if len(parts) < 2:
                continue
                
            day = parts[0].capitalize()
            shift_type = parts[1]
            
            # Get shift label from event configuration
            shift_label = "Unknown shift"
            if event_data.get('form_config'):
                for field in event_data['form_config']:
                    if field.get('type') == 'shift-selector' and field.get('schedule'):
                        schedule = field['schedule']
                        if day.lower() in schedule and schedule[day.lower()].get('shifts'):
                            shifts_config = schedule[day.lower()]['shifts']
                            if shift_type in shifts_config and shifts_config[shift_type].get('label'):
                                shift_label = shifts_config[shift_type]['label']
            
            shift_details.append({
                "day": day,
                "time": shift_label
            })
        
        # Check if webcal protocol is requested
        use_webcal = request.args.get('webcal', 'false').lower() == 'true'
        
        # Check if a specific calendar app is requested
        calendar_app = request.args.get('app', '').lower()
        
        # Generate iCalendar file with the appropriate calendar type
        ical_data = generate_ical_file(event_data, volunteer_data, shift_details, calendar_app)
        
        # Create a response
        event_name = event_data.get('event_name', 'Volunteer Event')
        sanitized_event_name = ''.join(c if c.isalnum() else '_' for c in event_name)
        
        response = Response(ical_data)
        
        # Set appropriate content type and disposition based on the calendar app
        if calendar_app == 'outlook':
            # For Outlook Calendar - specific headers for Outlook compatibility
            response.headers['Content-Type'] = 'text/calendar; charset=utf-8; method=REQUEST; component=VEVENT'
            response.headers['Content-Disposition'] = f'attachment; filename="{sanitized_event_name}_outlook.ics"'
            # Add Outlook-specific headers
            response.headers['X-MS-OLK-FORCEINSPECTOROPEN'] = 'TRUE'
            # Allow CORS for Outlook web access
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        elif calendar_app == 'apple':
            # For Apple Calendar
            response.headers['Content-Type'] = 'text/calendar; charset=utf-8'
            response.headers['Content-Disposition'] = f'inline; filename="{sanitized_event_name}_apple.ics"'
        elif use_webcal:
            # For generic webcal protocol
            response.headers['Content-Type'] = 'text/calendar; charset=utf-8'
            response.headers['Content-Disposition'] = f'inline; filename="{sanitized_event_name}_volunteer_shifts.ics"'
        else:
            # For direct download
            response.headers['Content-Type'] = 'text/calendar; charset=utf-8'
            response.headers['Content-Disposition'] = f'attachment; filename="{sanitized_event_name}_volunteer_shifts.ics"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating calendar: {str(e)}")
        return jsonify({"error": str(e)}), 500

@form_bp.route("/api/calendar-url/<event_id>/<email>", methods=["GET"])
def get_calendar_url(event_id, email):
    """
    Generate a Google Calendar URL for a volunteer's shifts.
    
    Args:
        event_id (str): The ID of the event
        email (str): The email of the volunteer
        
    Returns:
        json: Google Calendar URL
    """
    try:
        # Get event data
        events_collection = get_db().events
        event_data = events_collection.find_one({"event_id": event_id})
        
        if not event_data:
            return jsonify({"error": "Event not found"}), 404
        
        # Get volunteer data
        volunteer_collection = get_volunteer_collection(event_id)
        volunteer_data = volunteer_collection.find_one({"email": email})
        
        if not volunteer_data:
            return jsonify({"error": "Volunteer not found"}), 404
        
        # Extract shift information
        shifts = volunteer_data.get("shifts", {})
        
        # Convert shifts to a format suitable for calendar generation
        shift_details = []
        
        for shift_key, selected in shifts.items():
            if not selected:
                continue
                
            # Parse shift key (e.g., "monday_shift1")
            parts = shift_key.split('_')
            if len(parts) < 2:
                continue
                
            day = parts[0].capitalize()
            shift_type = parts[1]
            
            # Get shift label from event configuration
            shift_label = "Unknown shift"
            if event_data.get('form_config'):
                for field in event_data['form_config']:
                    if field.get('type') == 'shift-selector' and field.get('schedule'):
                        schedule = field['schedule']
                        if day.lower() in schedule and schedule[day.lower()].get('shifts'):
                            shifts_config = schedule[day.lower()]['shifts']
                            if shift_type in shifts_config and shifts_config[shift_type].get('label'):
                                shift_label = shifts_config[shift_type]['label']
            
            shift_details.append({
                "day": day,
                "time": shift_label
            })
        
        # Generate Google Calendar URL
        calendar_url = generate_google_calendar_url(event_data, volunteer_data, shift_details)
        
        if not calendar_url:
            return jsonify({"error": "Could not generate calendar URL"}), 400
        
        return jsonify({"url": calendar_url})
        
    except Exception as e:
        logger.error(f"Error generating calendar URL: {str(e)}")
        return jsonify({"error": str(e)}), 500
