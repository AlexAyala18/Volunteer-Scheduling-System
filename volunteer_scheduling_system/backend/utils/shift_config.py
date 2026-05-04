# backend/utils/shift_config.py

def get_shift_labels(event_config=None):
    """
    Returns a dictionary of shift labels that can be used across the application.
    
    Args:
        event_config (dict, optional): The event configuration containing dynamic shift times.
            If provided, will use the dynamic shift times instead of defaults.
    
    Returns:
        dict: A dictionary mapping shift keys to their display labels
    """
    # Default shift labels if no event configuration is provided
    default_labels = {
        "monday_shift1": "Mon 7:30-12:30", 
        "monday_shift2": "Mon 12:30-4:00", 
        "monday_shift3": "Mon All Day",
        "tuesday_shift1": "Tue 7:30-12:30", 
        "tuesday_shift2": "Tue 12:30-4:00", 
        "tuesday_shift3": "Tue All Day",
        "wednesday_shift1": "Wed 7:30-12:30", 
        "wednesday_shift2": "Wed 12:30-4:00", 
        "wednesday_shift3": "Wed All Day",
        "thursday_shift1": "Thu 7:30-12:30", 
        "thursday_shift2": "Thu 12:30-4:00", 
        "thursday_shift3": "Thu All Day",
        "friday_shift1": "Fri 7:30-12:30", 
        "friday_shift2": "Fri 12:30-4:00", 
        "friday_shift3": "Fri All Day",
        "saturday_shift1": "Sat 9:00-14:00",
        "saturday_shift2": "Sat All Day",
        "sunday_shift1": "Sun 9:00-14:00",
        "sunday_shift2": "Sun All Day"
    }
    
    # If no event configuration is provided, return the default labels
    if not event_config:
        return default_labels
        
    # Handle the case where event_config is not a dictionary or doesn't have form_config
    if not isinstance(event_config, dict):
        return default_labels
        
    # Try to extract dynamic shift labels from the event configuration
    dynamic_labels = {}
    
    # Find the shift-selector field in the form configuration
    form_config = event_config.get('form_config', [])
    if not form_config or not isinstance(form_config, list):
        return default_labels
        
    # Look for the shift-selector field
    shift_field = None
    for field in form_config:
        if isinstance(field, dict) and field.get('type') == 'shift-selector':
            shift_field = field
            break
            
    if not shift_field or not isinstance(shift_field.get('schedule'), dict):
        return default_labels
        
    schedule = shift_field.get('schedule', {})
    
    # Process each day in the schedule
    for day, day_config in schedule.items():
        if not isinstance(day_config, dict):
            continue
            
        if day_config.get('enabled') and isinstance(day_config.get('shifts'), dict):
            day_abbr = day[:3].capitalize()  # e.g., "monday" -> "Mon"
            
            # Process each shift for this day
            for shift_key, shift_config in day_config.get('shifts', {}).items():
                if not isinstance(shift_config, dict):
                    continue
                    
                if shift_config.get('enabled'):
                    # Use the label from the configuration, or a default if not available
                    label = shift_config.get('label')
                    if label:
                        full_key = f"{day}_{shift_key}"
                        dynamic_labels[full_key] = f"{day_abbr} {label}"
    
    # Merge the dynamic labels with the default labels, with dynamic labels taking precedence
    merged_labels = {**default_labels, **dynamic_labels}
    return merged_labels

def get_days():
    """
    Returns a list of days used in the shift system.
    """
    return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

def get_shift_times(event_config=None):
    """
    Returns a dictionary of shift times.
    
    Args:
        event_config (dict, optional): The event configuration containing dynamic shift times.
            If provided, will use the dynamic shift times instead of defaults.
            
    Returns:
        dict: A dictionary mapping shift keys to their display times
    """
    # Default shift times if no event configuration is provided
    default_times = {
        "shift1": "7:30 am - 12:30 pm",
        "shift2": "12:30 pm - 4:00 pm",
        "shift3": "All Day"
    }
    
    # If no event configuration is provided, return the default times
    if not event_config:
        return default_times
        
    # Handle the case where event_config is not a dictionary or doesn't have form_config
    if not isinstance(event_config, dict):
        return default_times
        
    # Try to extract dynamic shift times from the event configuration
    dynamic_times = {}
    
    # Find the shift-selector field in the form configuration
    form_config = event_config.get('form_config', [])
    if not form_config or not isinstance(form_config, list):
        return default_times
        
    # Look for the shift-selector field
    shift_field = None
    for field in form_config:
        if isinstance(field, dict) and field.get('type') == 'shift-selector':
            shift_field = field
            break
            
    if not shift_field or not isinstance(shift_field.get('schedule'), dict):
        return default_times
        
    schedule = shift_field.get('schedule', {})
    
    # Get all unique shift keys and their labels across all days
    for day, day_config in schedule.items():
        if not isinstance(day_config, dict):
            continue
            
        if day_config.get('enabled') and isinstance(day_config.get('shifts'), dict):
            # Process each shift for this day
            for shift_key, shift_config in day_config.get('shifts', {}).items():
                if not isinstance(shift_config, dict):
                    continue
                    
                if shift_config.get('enabled'):
                    # Use the label from the configuration, or a default if not available
                    label = shift_config.get('label')
                    if label:
                        # Extract just the shift number (e.g., "shift1" from "monday_shift1")
                        shift_num = shift_key
                        dynamic_times[shift_num] = label
    
    # Merge the dynamic times with the default times, with dynamic times taking precedence
    merged_times = {**default_times, **dynamic_times}
    return merged_times

def format_shifts_summary(shifts_data, event_config=None):
    """
    Formats a shifts dictionary into a human-readable summary string.
    
    Args:
        shifts_data (dict): Dictionary with shift keys and boolean values
        event_config (dict, optional): The event configuration containing dynamic shift times.
            If provided, will use the dynamic shift times instead of defaults.
        
    Returns:
        str: Comma-separated list of selected shifts
    """
    if not shifts_data or not isinstance(shifts_data, dict):
        return "None"
        
    shift_labels = get_shift_labels(event_config)
    selected = [label for key, label in shift_labels.items() if shifts_data.get(key)]
    
    return ", ".join(selected) if selected else "None"
