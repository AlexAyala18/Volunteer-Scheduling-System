"""
Calendar generator utility for creating iCalendar (.ics) files for volunteer shifts.
"""

import uuid
from datetime import datetime, timedelta
import pytz
from icalendar import Calendar, Event, vText

def create_ical_event(event_name, event_location, event_description, start_datetime, 
                     end_datetime, volunteer_name, shift_description=None, calendar_type=None):
    """
    Create an iCalendar event.
    
    Args:
        event_name (str): Name of the event
        event_location (str): Location of the event
        event_description (str): Description of the event
        start_datetime (datetime): Start date and time
        end_datetime (datetime): End date and time
        volunteer_name (str): Name of the volunteer
        shift_description (str, optional): Description of the specific shift
        calendar_type (str, optional): Type of calendar (apple, outlook, etc.)
        
    Returns:
        Event: An iCalendar Event object
    """
    cal_event = Event()
    
    # Create a unique identifier for this event
    cal_event.add('uid', str(uuid.uuid4()))
    
    # Set event basics
    cal_event.add('summary', f"{event_name} - Volunteer Shift")
    
    # Add location if available
    if event_location:
        cal_event.add('location', vText(event_location))
    
    # Set start and end times
    cal_event.add('dtstart', start_datetime)
    cal_event.add('dtend', end_datetime)
    
    # Set creation timestamp
    cal_event.add('dtstamp', datetime.now(pytz.utc))
    
    # Build description
    description = f"Volunteer: {volunteer_name}\n\n"
    
    if shift_description:
        description += f"Shift: {shift_description}\n\n"
        
    if event_description:
        description += f"Event Details: {event_description}\n\n"
        
    description += "Thank you for volunteering!"
    
    cal_event.add('description', description)
    
    # Add reminder (alarm) - 1 day before
    from icalendar import Alarm
    alarm = Alarm()
    alarm.add('action', 'DISPLAY')
    alarm.add('description', f"Reminder: Your volunteer shift for {event_name} is tomorrow")
    alarm.add('trigger', timedelta(days=-1))
    cal_event.add_component(alarm)
    
    # Add calendar-specific properties
    if calendar_type == 'outlook':
        # Add Outlook-specific properties
        cal_event.add('X-MICROSOFT-CDO-BUSYSTATUS', 'BUSY')
        cal_event.add('X-MICROSOFT-CDO-IMPORTANCE', '1')
        cal_event.add('X-MICROSOFT-DISALLOW-COUNTER', 'FALSE')
        cal_event.add('X-MS-OLK-CONFTYPE', '0')
        
        # Add organizer for Outlook
        cal_event.add('ORGANIZER;CN="Volunteer Coordinator"', 'mailto:volunteer@example.com')
        
        # Set status as confirmed for Outlook
        cal_event.add('STATUS', 'CONFIRMED')
    
    return cal_event

def generate_ical_file(event_data, volunteer_data, shift_details, calendar_type=None):
    """
    Generate an iCalendar file for a volunteer's shifts.
    
    Args:
        event_data (dict): Event information
        volunteer_data (dict): Volunteer information
        shift_details (list): List of shift details with day and time information
        
    Returns:
        bytes: iCalendar file content as bytes
    """
    # Create calendar
    cal = Calendar()
    cal.add('prodid', '-//Volunteer Scheduler//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    
    # Get event details
    event_name = event_data.get('event_name', 'Volunteer Event')
    event_location = event_data.get('event_location', '')
    event_description = event_data.get('event_description', '')
    
    # Get volunteer details
    volunteer_name = f"{volunteer_data.get('first_name', '')} {volunteer_data.get('last_name', '')}".strip()
    if not volunteer_name:
        volunteer_name = volunteer_data.get('email', 'Volunteer')
    
    # Process each shift
    for shift in shift_details:
        # Extract day and time information
        day = shift.get('day', '')  # e.g., "Monday"
        time_range = shift.get('time', '')  # e.g., "7:30 am - 12:30 pm"
        
        # Skip if missing required information
        if not day or not time_range:
            continue
        
        # Parse the event date
        event_start_date = event_data.get('event_start_date', '')
        if not event_start_date:
            continue
            
        # Convert to datetime object if it's a string
        if isinstance(event_start_date, str):
            try:
                event_start_date = datetime.fromisoformat(event_start_date.replace('Z', '+00:00'))
            except ValueError:
                # Try parsing as date only
                try:
                    event_start_date = datetime.strptime(event_start_date.split('T')[0], '%Y-%m-%d')
                except:
                    continue
        
        # Calculate the date for this shift based on day of week
        day_of_week = {
            'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 
            'Friday': 4, 'Saturday': 5, 'Sunday': 6
        }
        
        # Get the target day of week
        target_day = day_of_week.get(day, -1)
        if target_day == -1:
            continue
            
        # Calculate days to add to get to the target day
        current_day = event_start_date.weekday()
        days_to_add = (target_day - current_day) % 7
        
        shift_date = event_start_date + timedelta(days=days_to_add)
        
        # Parse the time range
        start_time, end_time = None, None
        
        if "All Day" in time_range:
            # All day event
            start_time = datetime.combine(shift_date.date(), datetime.min.time())
            end_time = datetime.combine(shift_date.date(), datetime.max.time())
        else:
            # Try to parse time range like "7:30 am - 12:30 pm"
            try:
                time_parts = time_range.split('-')
                if len(time_parts) == 2:
                    start_str = time_parts[0].strip()
                    end_str = time_parts[1].strip()
                    
                    # Parse start time
                    if 'am' in start_str.lower() or 'pm' in start_str.lower():
                        start_time = datetime.strptime(start_str, '%I:%M %p')
                    else:
                        start_time = datetime.strptime(start_str, '%H:%M')
                    
                    # Parse end time
                    if 'am' in end_str.lower() or 'pm' in end_str.lower():
                        end_time = datetime.strptime(end_str, '%I:%M %p')
                    else:
                        end_time = datetime.strptime(end_str, '%H:%M')
                    
                    # Combine date and time
                    start_datetime = datetime.combine(shift_date.date(), start_time.time())
                    end_datetime = datetime.combine(shift_date.date(), end_time.time())
                else:
                    # Can't parse time range, skip this shift
                    continue
            except Exception as e:
                print(f"Error parsing time range '{time_range}': {str(e)}")
                # Default to all day if we can't parse the time
                start_datetime = datetime.combine(shift_date.date(), datetime.min.time())
                end_datetime = datetime.combine(shift_date.date(), datetime.max.time())
        
        # Create the calendar event
        shift_description = f"{day} {time_range}"
        cal_event = create_ical_event(
            event_name, 
            event_location, 
            event_description, 
            start_datetime, 
            end_datetime, 
            volunteer_name, 
            shift_description,
            calendar_type
        )
        
        # Add the event to the calendar
        cal.add_component(cal_event)
    
    # Return the calendar as bytes
    return cal.to_ical()

def generate_google_calendar_url(event_data, volunteer_data, shift_details):
    """
    Generate a Google Calendar URL for adding an event.
    
    Args:
        event_data (dict): Event information
        volunteer_data (dict): Volunteer information
        shift_details (list): List of shift details with day and time information
        
    Returns:
        str: Google Calendar URL
    """
    # This is a simplified version that creates one event for the first shift
    # For multiple shifts, you would need to create multiple URLs or use a different approach
    
    if not shift_details:
        return None
        
    # Get the first shift
    shift = shift_details[0]
    
    # Extract event details
    event_name = event_data.get('event_name', 'Volunteer Event')
    event_location = event_data.get('event_location', '')
    event_description = event_data.get('event_description', '')
    
    # Get volunteer details
    volunteer_name = f"{volunteer_data.get('first_name', '')} {volunteer_data.get('last_name', '')}".strip()
    if not volunteer_name:
        volunteer_name = volunteer_data.get('email', 'Volunteer')
    
    # Extract day and time information
    day = shift.get('day', '')  # e.g., "Monday"
    time_range = shift.get('time', '')  # e.g., "7:30 am - 12:30 pm"
    
    # Skip if missing required information
    if not day or not time_range:
        return None
    
    # Parse the event date
    event_start_date = event_data.get('event_start_date', '')
    if not event_start_date:
        return None
        
    # Convert to datetime object if it's a string
    if isinstance(event_start_date, str):
        try:
            event_start_date = datetime.fromisoformat(event_start_date.replace('Z', '+00:00'))
        except ValueError:
            # Try parsing as date only
            try:
                event_start_date = datetime.strptime(event_start_date.split('T')[0], '%Y-%m-%d')
            except:
                return None
    
    # Calculate the date for this shift based on day of week
    day_of_week = {
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 
        'Friday': 4, 'Saturday': 5, 'Sunday': 6
    }
    
    # Get the target day of week
    target_day = day_of_week.get(day, -1)
    if target_day == -1:
        return None
        
    # Calculate days to add to get to the target day
    current_day = event_start_date.weekday()
    days_to_add = (target_day - current_day) % 7
    
    shift_date = event_start_date + timedelta(days=days_to_add)
    
    # Format the date for Google Calendar
    formatted_date = shift_date.strftime('%Y%m%d')
    
    # Parse the time range
    start_time, end_time = None, None
    
    if "All Day" in time_range:
        # All day event
        start_time = "000000"
        end_time = "235959"
    else:
        # Try to parse time range like "7:30 am - 12:30 pm"
        try:
            time_parts = time_range.split('-')
            if len(time_parts) == 2:
                start_str = time_parts[0].strip()
                end_str = time_parts[1].strip()
                
                # Parse start time
                if 'am' in start_str.lower() or 'pm' in start_str.lower():
                    start_time = datetime.strptime(start_str, '%I:%M %p')
                else:
                    start_time = datetime.strptime(start_str, '%H:%M')
                
                # Parse end time
                if 'am' in end_str.lower() or 'pm' in end_str.lower():
                    end_time = datetime.strptime(end_str, '%I:%M %p')
                else:
                    end_time = datetime.strptime(end_str, '%H:%M')
                
                # Format times for Google Calendar
                start_time = start_time.strftime('%H%M%S')
                end_time = end_time.strftime('%H%M%S')
            else:
                # Can't parse time range, use all day
                start_time = "000000"
                end_time = "235959"
        except Exception as e:
            print(f"Error parsing time range '{time_range}': {str(e)}")
            # Default to all day if we can't parse the time
            start_time = "000000"
            end_time = "235959"
    
    # Build the description
    description = f"Volunteer: {volunteer_name}\\n\\n"
    description += f"Shift: {day} {time_range}\\n\\n"
    
    if event_description:
        description += f"Event Details: {event_description}\\n\\n"
        
    description += "Thank you for volunteering!"
    
    # Build the Google Calendar URL
    import urllib.parse
    
    base_url = "https://www.google.com/calendar/render?action=TEMPLATE"
    
    params = {
        'text': f"{event_name} - Volunteer Shift",
        'dates': f"{formatted_date}T{start_time}/{formatted_date}T{end_time}",
        'details': description,
        'location': event_location,
        'sf': 'true',
        'output': 'xml'
    }
    
    url = f"{base_url}&{urllib.parse.urlencode(params)}"
    
    return url
