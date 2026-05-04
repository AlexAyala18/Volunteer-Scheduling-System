# backend/utils/form_config_loader.py

from backend.models.mongo import get_event_collection

def load_form_config(event_id):
    """
    Fetches the form configuration for a given event_id.
    Returns a dictionary with keys: event_id, event_name, form_config.
    
    Args:
        event_id (str): The unique identifier for the event
        
    Returns:
        dict: The event data including form configuration
        
    Raises:
        ValueError: If event not found or form_config is invalid
    """
    if not event_id:
        raise ValueError("Event ID is required")
        
    event = get_event_collection().find_one({"event_id": event_id}, {"_id": 0})
    if not event:
        raise ValueError(f"Event with ID '{event_id}' not found.")
    
    form_config = event.get("form_config")
    if not form_config:
        raise ValueError(f"Event '{event_id}' has no form configuration.")
        
    if not isinstance(form_config, list):
        raise TypeError("Form configuration must be a list of field definitions.")
    
    # Validate each field in the form configuration
    required_fields = ["first_name", "last_name", "email", "phone"]
    found_fields = set()
    
    for field in form_config:
        # Each field must be a dictionary with at least type, name, and label
        if not isinstance(field, dict):
            raise TypeError("Each field in form_config must be a dictionary")
            
        if "type" not in field:
            raise ValueError("Each field must have a 'type' property")
            
        if "name" not in field:
            raise ValueError("Each field must have a 'name' property")
            
        if "label" not in field:
            raise ValueError("Each field must have a 'label' property")
            
        # Track required fields
        if field["name"] in required_fields:
            found_fields.add(field["name"])
            
        # Validate checkbox-group has options
        if field["type"] == "checkbox-group" and (
            "options" not in field or 
            not isinstance(field["options"], list) or 
            not field["options"]
        ):
            raise ValueError(f"Checkbox group '{field['name']}' must have options")
    
    # Ensure all required fields are present
    missing = set(required_fields) - found_fields
    if missing:
        raise ValueError(f"Form configuration missing required fields: {', '.join(missing)}")
    
    # Ensure shifts field is present
    if not any(field["name"] == "shifts" for field in form_config):
        raise ValueError("Form configuration must include a 'shifts' field")

    return event

def validate_form_submission(data):
    """
    Validates form submission data against required fields.
    
    Args:
        data (dict): The form submission data
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ["first_name", "last_name", "phone", "email", "shifts"]
    missing = [f for f in required_fields if not data.get(f)]
    
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
        
    # Validate email format (basic check)
    email = data.get("email", "")
    if email and "@" not in email:
        return False, "Invalid email format"
        
    return True, None
