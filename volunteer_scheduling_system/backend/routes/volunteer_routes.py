# backend/routes/volunteer_routes.py

from flask import Blueprint, render_template
from backend.models.mongo import get_event_collection

volunteer_bp = Blueprint("volunteer_routes", __name__, url_prefix="/volunteer")

@volunteer_bp.route("/events")
def events_list():
    """
    Render the public events listing page.
    
    Returns:
        str: Rendered HTML template with all active events
    """
    try:
        # Get all events from the database
        events_collection = get_event_collection()
        events = list(events_collection.find({}, {"_id": 0}))
        
        # Sort events by start date (most recent first)
        events.sort(key=lambda x: x.get('event_start_date', ''), reverse=True)
        
        return render_template("volunteer/events.html", events=events)
    except Exception as e:
        print(f"Error fetching events for public listing: {str(e)}")
        return render_template("error.html", 
                              error_title="Error Loading Events",
                              error_message="Could not load the events list. Please try again later.")

@volunteer_bp.route("/form/<event_id>")
def event_form(event_id):
    """
    Render the volunteer registration form for a specific event.
    
    Args:
        event_id (str): The ID of the event
        
    Returns:
        str: Rendered HTML template
    """
    return render_template("volunteer/event_form.html", event_id=event_id)
