"""
Email service module for sending notifications to volunteers and administrators.
"""

import os
import logging
import re
import base64
from datetime import datetime
from pathlib import Path
from flask import current_app, Flask
from flask_mail import Message

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_logo_as_base64(logo_name="laredo_public_health.png"):
    """
    Read the logo image file and convert it to base64 for embedding in emails.
    
    Args:
        logo_name (str): Name of the logo file in the static/img directory
        
    Returns:
        str: Base64 encoded image with data URI prefix, or None if file not found
    """
    try:
        # Construct the path to the logo file
        logo_path = Path(__file__).parent.parent.parent / "frontend" / "static" / "img" / logo_name
        
        # Check if the file exists
        if not logo_path.exists():
            logger.warning(f"Logo file not found: {logo_path}")
            return None
            
        # Read the file and convert to base64
        with open(logo_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            
        # Determine MIME type based on file extension
        mime_type = "image/png"  # Default to PNG
        if logo_name.lower().endswith(".jpg") or logo_name.lower().endswith(".jpeg"):
            mime_type = "image/jpeg"
        elif logo_name.lower().endswith(".gif"):
            mime_type = "image/gif"
            
        # Return the data URI
        return f"data:{mime_type};base64,{encoded}"
        
    except Exception as e:
        logger.error(f"Error reading logo file: {str(e)}")
        return None

class EmailService:
    """
    Service for sending emails to volunteers and administrators.
    """
    
    def __init__(self):
        """
        Initialize the email service.
        """
        # No need to store SMTP settings as we'll use Flask-Mail
        pass
    
    def send_email(self, to_email, subject, html_content, text_content=None, from_email=None, attachments=None):
        """
        Send an email with HTML and plain text content using Flask-Mail.
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            html_content (str): HTML content of the email
            text_content (str, optional): Plain text content (falls back to stripped HTML if not provided)
            from_email (str, optional): Sender email (defaults to MAIL_DEFAULT_SENDER)
            attachments (list, optional): List of attachment file paths or (filename, data) tuples
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Get Flask app context
            app = current_app._get_current_object()
            
            # Check if Flask-Mail is configured
            if not hasattr(app, 'mail'):
                logger.error("Cannot send email: Flask-Mail not configured")
                return False
            
            # Create message
            msg = Message(
                subject=subject,
                recipients=[to_email],
                sender=from_email or app.config.get('MAIL_DEFAULT_SENDER')
            )
            
            # Add plain text version (fallback to stripped HTML if not provided)
            if text_content is None:
                # Simple HTML stripping
                text_content = re.sub(r'<.*?>', '', html_content)
                text_content = text_content.replace('&nbsp;', ' ')
            
            msg.body = text_content
            msg.html = html_content
            
            # Add attachments if any
            if attachments:
                for attachment in attachments:
                    if isinstance(attachment, tuple) and len(attachment) == 2:
                        # (filename, data) tuple
                        filename, data = attachment
                        msg.attach(filename, 'application/octet-stream', data)
                    elif isinstance(attachment, (str, Path)):
                        # File path
                        path = Path(attachment)
                        if path.exists():
                            with open(path, 'rb') as f:
                                msg.attach(path.name, 'application/octet-stream', f.read())
                        else:
                            logger.warning(f"Attachment not found: {path}")
            
            # Send the email
            app.mail.send(msg)
            
            logger.info(f"Email sent to {to_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_volunteer_confirmation(self, volunteer_data, event_data, language="en"):
        """
        Send a confirmation email to a volunteer after they sign up.
        
        Args:
            volunteer_data (dict): Volunteer registration data
            event_data (dict): Event details
            language (str): Language preference ('en' for English, 'es' for Spanish)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        # Extract needed information
        email = volunteer_data.get('email')
        if not email:
            logger.error("Cannot send confirmation: volunteer email missing")
            return False
            
        first_name = volunteer_data.get('first_name', 'Volunteer')
        event_name = event_data.get('event_name', 'the event')
        event_date = event_data.get('event_start_date', 'the scheduled date')
        if isinstance(event_date, str) and 'T' in event_date:
            event_date = event_date.split('T')[0]
        
        location = event_data.get('event_location', 'the event location')
        
        # Format shift information
        shifts = volunteer_data.get('shifts', {})
        shift_details = []
        
        if shifts:
            for shift_key, selected in shifts.items():
                if selected:
                    # Parse shift key (e.g., "monday_shift1")
                    parts = shift_key.split('_')
                    if len(parts) >= 2:
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
                        
                        shift_details.append(f"{day}: {shift_label}")
        
        shift_text = "\n".join([f"- {shift}" for shift in shift_details]) if shift_details else "No specific shifts selected"
        
        # Get the logo as base64
        logo_base64 = get_logo_as_base64("laredo_public_health.png")
        logo_img_tag = f'<img src="{logo_base64}" alt="City of Laredo Public Health Department" class="logo" style="margin: 10px auto; display: block; max-width: 200px;">'
        
        # Create email content based on language preference
        if language == "es":
            # Spanish version
            subject = f"¡Gracias por ser voluntario con {event_name}!"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Confirmación de Voluntario</title>
                <style>
                    /* Base styles */
                    body, html {{ margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #F5F5F5; }}
                    
                    /* Container */
                    .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
                    
                    /* Header */
                    .header {{ background-color: #1E3A5F; color: white; padding: 20px; text-align: center; }}
                    .header h1 {{ margin: 0; padding: 10px 0; font-size: 24px; }}
                    
                    /* Content */
                    .content {{ padding: 20px 30px; background-color: white; }}
                    
                    /* Details box */
                    .details {{ background-color: #f0f8ff; padding: 20px; border-left: 4px solid #1E3A5F; margin: 20px 0; border-radius: 0 4px 4px 0; }}
                    .details h2 {{ margin-top: 0; color: #1E3A5F; font-size: 18px; }}
                    
                    /* Typography */
                    h1, h2, h3 {{ color: #1E3A5F; }}
                    p {{ margin: 10px 0; }}
                    strong {{ color: #1E3A5F; font-weight: bold; }}
                    ul {{ margin: 15px 0; padding-left: 25px; }}
                    li {{ margin-bottom: 8px; }}
                    
                    /* Footer */
                    .footer {{ text-align: center; margin-top: 30px; padding: 15px; border-top: 1px solid #eee; color: #666; font-size: 12px; }}
                    
                    /* Button */
                    .btn {{ display: inline-block; background-color: #F7931E; color: white; padding: 12px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; margin-top: 20px; text-align: center; }}
                    
                    /* Mobile responsiveness */
                    @media only screen and (max-width: 480px) {{
                        .container {{ width: 100%; border-radius: 0; }}
                        .content {{ padding: 15px; }}
                        .details {{ padding: 15px; }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img_tag}
                        <h1>Confirmación de Voluntario</h1>
                    </div>
                    <div class="content">
                        <p>Hola {first_name},</p>
                        
                        <p>¡Gracias por inscribirte como voluntario en <strong>{event_name}</strong>! Tu apoyo hace una diferencia en nuestra comunidad.</p>
                        
                        <div class="details">
                            <h2>Tus Detalles de Voluntario:</h2>
                            <p><strong>Evento:</strong> {event_name}</p>
                            <p><strong>Fecha:</strong> {event_date}</p>
                            <p><strong>Ubicación:</strong> {location}</p>
                            <p><strong>Tu(s) Turno(s):</strong></p>
                            <p>{shift_text}</p>
                        </div>
                        
                        <p>Qué Traer:</p>
                        <ul>
                            <li>Ropa y zapatos cómodos</li>
                            <li>Botella de agua</li>
                            <li>Actitud positiva</li>
                        </ul>
                        
                        <p>Si tienes alguna pregunta o necesitas hacer cambios en tu registro, por favor contacta al coordinador del evento.</p>
                        
                        <p>¡Gracias por tu compromiso de servir a nuestra comunidad!</p>
                    </div>
                    <div class="footer">
                        <p>&copy; {datetime.now().year} Sistema de Voluntarios - Salud Pública de Laredo</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
            ¡Gracias por ser voluntario con {event_name}!
            
            Hola {first_name},
            
            ¡Gracias por inscribirte como voluntario en {event_name}! Tu apoyo hace una diferencia en nuestra comunidad.
            
            Tus Detalles de Voluntario:
            - Evento: {event_name}
            - Fecha: {event_date}
            - Ubicación: {location}
            - Tu(s) Turno(s):
            {shift_text}
            
            Qué Traer:
            - Ropa y zapatos cómodos
            - Botella de agua
            - Actitud positiva
            
            Si tienes alguna pregunta o necesitas hacer cambios en tu registro, por favor contacta al coordinador del evento.
            
            ¡Gracias por tu compromiso de servir a nuestra comunidad!
            
            Sistema de Voluntarios - Salud Pública de Laredo
            """
        else:
            # English version (default)
            subject = f"Thank you for volunteering with {event_name}!"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Volunteer Confirmation</title>
                <style>
                    /* Base styles */
                    body, html {{ margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #F5F5F5; }}
                    
                    /* Container */
                    .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
                    
                    /* Header */
                    .header {{ background-color: #1E3A5F; color: white; padding: 20px; text-align: center; }}
                    .header h1 {{ margin: 0; padding: 10px 0; font-size: 24px; }}
                    
                    /* Content */
                    .content {{ padding: 20px 30px; background-color: white; }}
                    
                    /* Details box */
                    .details {{ background-color: #f0f8ff; padding: 20px; border-left: 4px solid #1E3A5F; margin: 20px 0; border-radius: 0 4px 4px 0; }}
                    .details h2 {{ margin-top: 0; color: #1E3A5F; font-size: 18px; }}
                    
                    /* Typography */
                    h1, h2, h3 {{ color: #1E3A5F; }}
                    p {{ margin: 10px 0; }}
                    strong {{ color: #1E3A5F; font-weight: bold; }}
                    ul {{ margin: 15px 0; padding-left: 25px; }}
                    li {{ margin-bottom: 8px; }}
                    
                    /* Footer */
                    .footer {{ text-align: center; margin-top: 30px; padding: 15px; border-top: 1px solid #eee; color: #666; font-size: 12px; }}
                    
                    /* Button */
                    .btn {{ display: inline-block; background-color: #F7931E; color: white; padding: 12px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; margin-top: 20px; text-align: center; }}
                    
                    /* Mobile responsiveness */
                    @media only screen and (max-width: 480px) {{
                        .container {{ width: 100%; border-radius: 0; }}
                        .content {{ padding: 15px; }}
                        .details {{ padding: 15px; }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img_tag}
                        <h1>Volunteer Confirmation</h1>
                    </div>
                    <div class="content">
                        <p>Hi {first_name},</p>
                        
                        <p>Thank you for signing up to volunteer at <strong>{event_name}</strong>! Your support makes a difference in our community.</p>
                        
                        <div class="details">
                            <h2>Your Volunteer Details:</h2>
                            <p><strong>Event:</strong> {event_name}</p>
                            <p><strong>Date:</strong> {event_date}</p>
                            <p><strong>Location:</strong> {location}</p>
                            <p><strong>Your Shift(s):</strong></p>
                            <p>{shift_text}</p>
                        </div>
                        
                        <p>What to Bring:</p>
                        <ul>
                            <li>Comfortable clothes and shoes</li>
                            <li>Water bottle</li>
                            <li>Positive attitude</li>
                        </ul>
                        
                        <p>If you have any questions or need to make changes to your registration, please contact the event coordinator.</p>
                        
                        <p>Thank you for your commitment to serving our community!</p>
                    </div>
                    <div class="footer">
                        <p>&copy; {datetime.now().year} Volunteer System - Laredo Public Health</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
            Thank you for volunteering with {event_name}!
            
            Hi {first_name},
            
            Thank you for signing up to volunteer at {event_name}! Your support makes a difference in our community.
            
            Your Volunteer Details:
            - Event: {event_name}
            - Date: {event_date}
            - Location: {location}
            - Your Shift(s):
            {shift_text}
            
            What to Bring:
            - Comfortable clothes and shoes
            - Water bottle
            - Positive attitude
            
            If you have any questions or need to make changes to your registration, please contact the event coordinator.
            
            Thank you for your commitment to serving our community!
            
            Volunteer System - Laredo Public Health
            """
        
        # Send the email
        return self.send_email(
            to_email=email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )
    
    def send_reminder_email(self, volunteer_data, event_data, reminder_type='day_before', language="en"):
        """
        Send a reminder email to a volunteer before their shift.
        
        Args:
            volunteer_data (dict): Volunteer registration data
            event_data (dict): Event details
            reminder_type (str): Type of reminder ('week_before', 'day_before')
            language (str): Language preference ('en' for English, 'es' for Spanish)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        # Extract needed information
        email = volunteer_data.get('email')
        if not email:
            logger.error("Cannot send reminder: volunteer email missing")
            return False
            
        first_name = volunteer_data.get('first_name', 'Volunteer')
        event_name = event_data.get('event_name', 'the event')
        event_date = event_data.get('event_start_date', 'the scheduled date')
        if isinstance(event_date, str) and 'T' in event_date:
            event_date = event_date.split('T')[0]
        
        location = event_data.get('event_location', 'the event location')
        
        # Format shift information (same as confirmation email)
        shifts = volunteer_data.get('shifts', {})
        shift_details = []
        
        if shifts:
            for shift_key, selected in shifts.items():
                if selected:
                    parts = shift_key.split('_')
                    if len(parts) >= 2:
                        day = parts[0].capitalize()
                        shift_type = parts[1]
                        
                        shift_label = "Unknown shift"
                        if event_data.get('form_config'):
                            for field in event_data['form_config']:
                                if field.get('type') == 'shift-selector' and field.get('schedule'):
                                    schedule = field['schedule']
                                    if day.lower() in schedule and schedule[day.lower()].get('shifts'):
                                        shifts_config = schedule[day.lower()]['shifts']
                                        if shift_type in shifts_config and shifts_config[shift_type].get('label'):
                                            shift_label = shifts_config[shift_type]['label']
                        
                        shift_details.append(f"{day}: {shift_label}")
        
        shift_text = "\n".join([f"- {shift}" for shift in shift_details]) if shift_details else "No specific shifts selected"
        
        # Get the logo as base64
        logo_base64 = get_logo_as_base64("laredo_public_health.png")
        logo_img_tag = f'<img src="{logo_base64}" alt="City of Laredo Public Health Department" class="logo" style="margin: 10px auto; display: block; max-width: 200px;">'
        
        # Create email content based on reminder type and language
        if language == "es":
            # Spanish version
            if reminder_type == 'week_before':
                subject = f"Recordatorio: Tu próximo turno de voluntario en {event_name}"
                
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Recordatorio de Voluntario</title>
                    <style>
                        /* Base styles */
                        body, html {{ margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #F5F5F5; }}
                        
                        /* Container */
                        .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
                        
                        /* Header */
                        .header {{ background-color: #1E3A5F; color: white; padding: 20px; text-align: center; }}
                        .header h1 {{ margin: 0; padding: 10px 0; font-size: 24px; }}
                        
                        /* Content */
                        .content {{ padding: 20px 30px; background-color: white; }}
                        
                        /* Details box */
                        .details {{ background-color: #f0f8ff; padding: 20px; border-left: 4px solid #1E3A5F; margin: 20px 0; border-radius: 0 4px 4px 0; }}
                        .details h2 {{ margin-top: 0; color: #1E3A5F; font-size: 18px; }}
                        
                        /* Typography */
                        h1, h2, h3 {{ color: #1E3A5F; }}
                        p {{ margin: 10px 0; }}
                        strong {{ color: #1E3A5F; font-weight: bold; }}
                        ul {{ margin: 15px 0; padding-left: 25px; }}
                        li {{ margin-bottom: 8px; }}
                        
                        /* Footer */
                        .footer {{ text-align: center; margin-top: 30px; padding: 15px; border-top: 1px solid #eee; color: #666; font-size: 12px; }}
                        
                        /* Button */
                        .btn {{ display: inline-block; background-color: #F7931E; color: white; padding: 12px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; margin-top: 20px; text-align: center; }}
                        
                        /* Mobile responsiveness */
                        @media only screen and (max-width: 480px) {{
                            .container {{ width: 100%; border-radius: 0; }}
                            .content {{ padding: 15px; }}
                            .details {{ padding: 15px; }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            {logo_img_tag}
                            <h1>Recordatorio de Voluntario</h1>
                        </div>
                        <div class="content">
                            <p>Hola {first_name},</p>
                            
                            <p>Este es un recordatorio amistoso de que estás programado para ser voluntario en <strong>{event_name}</strong> en una semana.</p>
                            
                            <div class="details">
                                <h2>Detalles del Evento:</h2>
                                <p><strong>Evento:</strong> {event_name}</p>
                                <p><strong>Fecha:</strong> {event_date}</p>
                                <p><strong>Ubicación:</strong> {location}</p>
                                <p><strong>Tu(s) Turno(s):</strong></p>
                                <p>{shift_text}</p>
                            </div>
                            
                            <p>Información Importante:</p>
                            <ul>
                                <li>Por favor llega 15 minutos antes de que comience tu turno</li>
                                <li>Usa ropa cómoda y zapatos cerrados</li>
                                <li>Trae una botella de agua y cualquier artículo personal necesario</li>
                            </ul>
                            
                            <p>Si ya no puedes asistir, por favor háznos saber lo antes posible respondiendo a este correo electrónico.</p>
                            
                            <p>¡Gracias por tu compromiso con nuestra comunidad!</p>
                        </div>
                        <div class="footer">
                            <p>&copy; {datetime.now().year} Sistema de Voluntarios - Salud Pública de Laredo</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                text_content = f"""
                Recordatorio: Tu próximo turno de voluntario en {event_name}
                
                Hola {first_name},
                
                Este es un recordatorio amistoso de que estás programado para ser voluntario en {event_name} en una semana.
                
                Detalles del Evento:
                - Evento: {event_name}
                - Fecha: {event_date}
                - Ubicación: {location}
                - Tu(s) Turno(s):
                {shift_text}
                
                Información Importante:
                - Por favor llega 15 minutos antes de que comience tu turno
                - Usa ropa cómoda y zapatos cerrados
                - Trae una botella de agua y cualquier artículo personal necesario
                
                Si ya no puedes asistir, por favor háznos saber lo antes posible respondiendo a este correo electrónico.
                
                ¡Gracias por tu compromiso con nuestra comunidad!
                
                Sistema de Voluntarios - Salud Pública de Laredo
                """
                
            elif reminder_type == 'day_before':
                subject = f"MAÑANA: Tu turno de voluntario en {event_name}"
                
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Recordatorio de Voluntario</title>
                    <style>
                        /* Base styles */
                        body, html {{ margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #F5F5F5; }}
                        
                        /* Container */
                        .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
                        
                        /* Header */
                        .header {{ background-color: #1E3A5F; color: white; padding: 20px; text-align: center; }}
                        .header h1 {{ margin: 0; padding: 10px 0; font-size: 24px; }}
                        
                        /* Content */
                        .content {{ padding: 20px 30px; background-color: white; }}
                        
                        /* Details box */
                        .details {{ background-color: #f0f8ff; padding: 20px; border-left: 4px solid #1E3A5F; margin: 20px 0; border-radius: 0 4px 4px 0; }}
                        .details h2 {{ margin-top: 0; color: #1E3A5F; font-size: 18px; }}
                        
                        /* Important box */
                        .important {{ background-color: #fff0f0; padding: 20px; border-left: 4px solid #F7931E; margin: 20px 0; border-radius: 0 4px 4px 0; }}
                        .important h3 {{ margin-top: 0; color: #F7931E; font-size: 16px; }}
                        
                        /* Typography */
                        h1, h2, h3 {{ color: #1E3A5F; }}
                        p {{ margin: 10px 0; }}
                        strong {{ color: #1E3A5F; font-weight: bold; }}
                        ul {{ margin: 15px 0; padding-left: 25px; }}
                        li {{ margin-bottom: 8px; }}
                        
                        /* Footer */
                        .footer {{ text-align: center; margin-top: 30px; padding: 15px; border-top: 1px solid #eee; color: #666; font-size: 12px; }}
                        
                        /* Mobile responsiveness */
                        @media only screen and (max-width: 480px) {{
                            .container {{ width: 100%; border-radius: 0; }}
                            .content {{ padding: 15px; }}
                            .details, .important {{ padding: 15px; }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            {logo_img_tag}
                            <h1>Recordatorio de Voluntario</h1>
                        </div>
                        <div class="content">
                            <p>Hola {first_name},</p>
                            
                            <p>¡Este es un recordatorio importante de que estás programado para ser voluntario en <strong>{event_name}</strong> MAÑANA!</p>
                            
                            <div class="details">
                                <h2>Detalles del Evento:</h2>
                                <p><strong>Evento:</strong> {event_name}</p>
                                <p><strong>Fecha:</strong> {event_date}</p>
                                <p><strong>Ubicación:</strong> {location}</p>
                                <p><strong>Tu(s) Turno(s):</strong></p>
                                <p>{shift_text}</p>
                            </div>
                            
                            <div class="important">
                                <h3>Recordatorios Importantes:</h3>
                                <ul>
                                    <li>Por favor llega 15 minutos antes de que comience tu turno</li>
                                    <li>Trae una identificación con foto</li>
                                    <li>Usa ropa cómoda y zapatos cerrados</li>
                                    <li>Trae una botella de agua</li>
                                </ul>
                            </div>
                            
                            <p>Si ya no puedes asistir, por favor háznos saber <strong>INMEDIATAMENTE</strong> respondiendo a este correo electrónico.</p>
                            
                            <p>¡Gracias por tu compromiso con nuestra comunidad! Esperamos verte mañana.</p>
                        </div>
                        <div class="footer">
                            <p>&copy; {datetime.now().year} Sistema de Voluntarios - Salud Pública de Laredo</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                text_content = f"""
                MAÑANA: Tu turno de voluntario en {event_name}
                
                Hola {first_name},
                
                ¡Este es un recordatorio importante de que estás programado para ser voluntario en {event_name} MAÑANA!
                
                Detalles del Evento:
                - Evento: {event_name}
                - Fecha: {event_date}
                - Ubicación: {location}
                - Tu(s) Turno(s):
                {shift_text}
                
                Recordatorios Importantes:
                - Por favor llega 15 minutos antes de que comience tu turno
                - Trae una identificación con foto
                - Usa ropa cómoda y zapatos cerrados
                - Trae una botella de agua
                
                Si ya no puedes asistir, por favor háznos saber INMEDIATAMENTE respondiendo a este correo electrónico.
                
                ¡Gracias por tu compromiso con nuestra comunidad! Esperamos verte mañana.
                
                Sistema de Voluntarios - Salud Pública de Laredo
                """
        else:
            # English version (default)
            if reminder_type == 'week_before':
                subject = f"Reminder: Your upcoming volunteer shift at {event_name}"
                
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Volunteer Reminder</title>
                    <style>
                        /* Base styles */
                        body, html {{ margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #F5F5F5; }}
                        
                        /* Container */
                        .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
                        
                        /* Header */
                        .header {{ background-color: #1E3A5F; color: white; padding: 20px; text-align: center; }}
                        .header h1 {{ margin: 0; padding: 10px 0; font-size: 24px; }}
                        
                        /* Content */
                        .content {{ padding: 20px 30px; background-color: white; }}
                        
                        /* Details box */
                        .details {{ background-color: #f0f8ff; padding: 20px; border-left: 4px solid #1E3A5F; margin: 20px 0; border-radius: 0 4px 4px 0; }}
                        .details h2 {{ margin-top: 0; color: #1E3A5F; font-size: 18px; }}
                        
                        /* Typography */
                        h1, h2, h3 {{ color: #1E3A5F; }}
                        p {{ margin: 10px 0; }}
                        strong {{ color: #1E3A5F; font-weight: bold; }}
                        ul {{ margin: 15px 0; padding-left: 25px; }}
                        li {{ margin-bottom: 8px; }}
                        
                        /* Footer */
                        .footer {{ text-align: center; margin-top: 30px; padding: 15px; border-top: 1px solid #eee; color: #666; font-size: 12px; }}
                        
                        /* Button */
                        .btn {{ display: inline-block; background-color: #F7931E; color: white; padding: 12px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; margin-top: 20px; text-align: center; }}
                        
                        /* Mobile responsiveness */
                        @media only screen and (max-width: 480px) {{
                            .container {{ width: 100%; border-radius: 0; }}
                            .content {{ padding: 15px; }}
                            .details {{ padding: 15px; }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            {logo_img_tag}
                            <h1>Volunteer Reminder</h1>
                        </div>
                        <div class="content">
                            <p>Hi {first_name},</p>
                            
                            <p>This is a friendly reminder that you are scheduled to volunteer at <strong>{event_name}</strong> in one week.</p>
                            
                            <div class="details">
                                <h2>Event Details:</h2>
                                <p><strong>Event:</strong> {event_name}</p>
                                <p><strong>Date:</strong> {event_date}</p>
                                <p><strong>Location:</strong> {location}</p>
                                <p><strong>Your Shift(s):</strong></p>
                                <p>{shift_text}</p>
                            </div>
                            
                            <p>Important Information:</p>
                            <ul>
                                <li>Please arrive 15 minutes before your shift begins</li>
                                <li>Wear comfortable clothing and closed-toe shoes</li>
                                <li>Bring a water bottle and any necessary personal items</li>
                            </ul>
                            
                            <p>If you can no longer attend, please let us know as soon as possible by replying to this email.</p>
                            
                            <p>Thank you for your commitment to our community!</p>
                        </div>
                        <div class="footer">
                            <p>&copy; {datetime.now().year} Volunteer System - Laredo Public Health</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                text_content = f"""
                Reminder: Your upcoming volunteer shift at {event_name}
                
                Hi {first_name},
                
                This is a friendly reminder that you are scheduled to volunteer at {event_name} in one week.
                
                Event Details:
                - Event: {event_name}
                - Date: {event_date}
                - Location: {location}
                - Your Shift(s):
                {shift_text}
                
                Important Information:
                - Please arrive 15 minutes before your shift begins
                - Wear comfortable clothing and closed-toe shoes
                - Bring a water bottle and any necessary personal items
                
                If you can no longer attend, please let us know as soon as possible by replying to this email.
                
                Thank you for your commitment to our community!
                
                Volunteer System - Laredo Public Health
                """
                
            elif reminder_type == 'day_before':
                subject = f"TOMORROW: Your volunteer shift at {event_name}"
                
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Volunteer Reminder</title>
                    <style>
                        /* Base styles */
                        body, html {{ margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #F5F5F5; }}
                        
                        /* Container */
                        .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
                        
                        /* Header */
                        .header {{ background-color: #1E3A5F; color: white; padding: 20px; text-align: center; }}
                        .header h1 {{ margin: 0; padding: 10px 0; font-size: 24px; }}
                        
                        /* Content */
                        .content {{ padding: 20px 30px; background-color: white; }}
                        
                        /* Details box */
                        .details {{ background-color: #f0f8ff; padding: 20px; border-left: 4px solid #1E3A5F; margin: 20px 0; border-radius: 0 4px 4px 0; }}
                        .details h2 {{ margin-top: 0; color: #1E3A5F; font-size: 18px; }}
                        
                        /* Important box */
                        .important {{ background-color: #fff0f0; padding: 20px; border-left: 4px solid #F7931E; margin: 20px 0; border-radius: 0 4px 4px 0; }}
                        .important h3 {{ margin-top: 0; color: #F7931E; font-size: 16px; }}
                        
                        /* Typography */
                        h1, h2, h3 {{ color: #1E3A5F; }}
                        p {{ margin: 10px 0; }}
                        strong {{ color: #1E3A5F; font-weight: bold; }}
                        ul {{ margin: 15px 0; padding-left: 25px; }}
                        li {{ margin-bottom: 8px; }}
                        
                        /* Footer */
                        .footer {{ text-align: center; margin-top: 30px; padding: 15px; border-top: 1px solid #eee; color: #666; font-size: 12px; }}
                        
                        /* Mobile responsiveness */
                        @media only screen and (max-width: 480px) {{
                            .container {{ width: 100%; border-radius: 0; }}
                            .content {{ padding: 15px; }}
                            .details, .important {{ padding: 15px; }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            {logo_img_tag}
                            <h1>Volunteer Reminder</h1>
                        </div>
                        <div class="content">
                            <p>Hi {first_name},</p>
                            
                            <p>This is an important reminder that you are scheduled to volunteer at <strong>{event_name}</strong> TOMORROW!</p>
                            
                            <div class="details">
                                <h2>Event Details:</h2>
                                <p><strong>Event:</strong> {event_name}</p>
                                <p><strong>Date:</strong> {event_date}</p>
                                <p><strong>Location:</strong> {location}</p>
                                <p><strong>Your Shift(s):</strong></p>
                                <p>{shift_text}</p>
                            </div>
                            
                            <div class="important">
                                <h3>Important Reminders:</h3>
                                <ul>
                                    <li>Please arrive 15 minutes before your shift begins</li>
                                    <li>Bring a photo ID</li>
                                    <li>Wear comfortable clothing and closed-toe shoes</li>
                                    <li>Bring a water bottle</li>
                                </ul>
                            </div>
                            
                            <p>If you can no longer attend, please let us know <strong>IMMEDIATELY</strong> by replying to this email.</p>
                            
                            <p>Thank you for your commitment to our community! We look forward to seeing you tomorrow.</p>
                        </div>
                        <div class="footer">
                            <p>&copy; {datetime.now().year} Volunteer System - Laredo Public Health</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                text_content = f"""
                TOMORROW: Your volunteer shift at {event_name}
                
                Hi {first_name},
                
                This is an important reminder that you are scheduled to volunteer at {event_name} TOMORROW!
                
                Event Details:
                - Event: {event_name}
                - Date: {event_date}
                - Location: {location}
                - Your Shift(s):
                {shift_text}
                
                Important Reminders:
                - Please arrive 15 minutes before your shift begins
                - Bring a photo ID
                - Wear comfortable clothing and closed-toe shoes
                - Bring a water bottle
                
                If you can no longer attend, please let us know IMMEDIATELY by replying to this email.
                
                Thank you for your commitment to our community! We look forward to seeing you tomorrow.
                
                Volunteer System - Laredo Public Health
                """
        
        # Send the email
        return self.send_email(
            to_email=email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )
    
    def send_thank_you_email(self, volunteer_data, event_data, language="en"):
        """
        Send a thank you email to a volunteer after the event.
        
        Args:
            volunteer_data (dict): Volunteer registration data
            event_data (dict): Event details
            language (str): Language preference ('en' for English, 'es' for Spanish)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        # Extract needed information
        email = volunteer_data.get('email')
        if not email:
            logger.error("Cannot send thank you email: volunteer email missing")
            return False
            
        first_name = volunteer_data.get('first_name', 'Volunteer')
        event_name = event_data.get('event_name', 'the event')
        
        # Get the logo as base64
        logo_base64 = get_logo_as_base64("laredo_public_health.png")
        logo_img_tag = f'<img src="{logo_base64}" alt="City of Laredo Public Health Department" class="logo" style="margin: 10px auto; display: block; max-width: 200px;">'
        
        # Create email content based on language preference
        if language == "es":
            # Spanish version
            subject = f"¡Gracias por tu servicio en {event_name}!"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Agradecimiento por Voluntariado</title>
                <style>
                    /* Base styles */
                    body, html {{ margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #F5F5F5; }}
                    
                    /* Container */
                    .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
                    
                    /* Header */
                    .header {{ background-color: #1E3A5F; color: white; padding: 20px; text-align: center; }}
                    .header h1 {{ margin: 0; padding: 10px 0; font-size: 24px; }}
                    
                    /* Content */
                    .content {{ padding: 20px 30px; background-color: white; }}
                    
                    /* Thank you box */
                    .thank-you {{ background-color: #f0fff0; padding: 20px; border-left: 4px solid #4CAF50; margin: 20px 0; border-radius: 0 4px 4px 0; }}
                    .thank-you h2 {{ margin-top: 0; color: #4CAF50; font-size: 18px; }}
                    
                    /* Typography */
                    h1, h2, h3 {{ color: #1E3A5F; }}
                    p {{ margin: 10px 0; }}
                    strong {{ color: #1E3A5F; font-weight: bold; }}
                    
                    /* Footer */
                    .footer {{ text-align: center; margin-top: 30px; padding: 15px; border-top: 1px solid #eee; color: #666; font-size: 12px; }}
                    
                    /* Button */
                    .btn {{ display: inline-block; background-color: #F7931E; color: white; padding: 12px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; margin-top: 20px; text-align: center; }}
                    
                    /* Mobile responsiveness */
                    @media only screen and (max-width: 480px) {{
                        .container {{ width: 100%; border-radius: 0; }}
                        .content {{ padding: 15px; }}
                        .thank-you {{ padding: 15px; }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img_tag}
                        <h1>¡Gracias por tu Servicio!</h1>
                    </div>
                    <div class="content">
                        <p>Hola {first_name},</p>
                        
                        <div class="thank-you">
                            <h2>¡Tu Contribución Hizo la Diferencia!</h2>
                            <p>Queremos expresar nuestro más sincero agradecimiento por tu tiempo y dedicación como voluntario en <strong>{event_name}</strong>. Tu servicio desinteresado ha tenido un impacto positivo en nuestra comunidad.</p>
                        </div>
                        
                        <p>Gracias a voluntarios como tú, podemos continuar brindando servicios esenciales y apoyo a nuestra comunidad. Tu disposición para dar tu tiempo y energía es verdaderamente inspiradora.</p>
                        
                        <p>Esperamos verte en futuros eventos. Tu continuo apoyo es invaluable para nosotros.</p>
                        
                        <p>Con gratitud,</p>
                        <p>El Equipo de Salud Pública de Laredo</p>
                    </div>
                    <div class="footer">
                        <p>&copy; {datetime.now().year} Sistema de Voluntarios - Salud Pública de Laredo</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
            ¡Gracias por tu servicio en {event_name}!
            
            Hola {first_name},
            
            ¡Tu Contribución Hizo la Diferencia!
            
            Queremos expresar nuestro más sincero agradecimiento por tu tiempo y dedicación como voluntario en {event_name}. Tu servicio desinteresado ha tenido un impacto positivo en nuestra comunidad.
            
            Gracias a voluntarios como tú, podemos continuar brindando servicios esenciales y apoyo a nuestra comunidad. Tu disposición para dar tu tiempo y energía es verdaderamente inspiradora.
            
            Esperamos verte en futuros eventos. Tu continuo apoyo es invaluable para nosotros.
            
            Con gratitud,
            El Equipo de Salud Pública de Laredo
            
            Sistema de Voluntarios - Salud Pública de Laredo
            """
        else:
            # English version (default)
            subject = f"Thank you for your service at {event_name}!"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Volunteer Thank You</title>
                <style>
                    /* Base styles */
                    body, html {{ margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #F5F5F5; }}
                    
                    /* Container */
                    .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
                    
                    /* Header */
                    .header {{ background-color: #1E3A5F; color: white; padding: 20px; text-align: center; }}
                    .header h1 {{ margin: 0; padding: 10px 0; font-size: 24px; }}
                    
                    /* Content */
                    .content {{ padding: 20px 30px; background-color: white; }}
                    
                    /* Thank you box */
                    .thank-you {{ background-color: #f0fff0; padding: 20px; border-left: 4px solid #4CAF50; margin: 20px 0; border-radius: 0 4px 4px 0; }}
                    .thank-you h2 {{ margin-top: 0; color: #4CAF50; font-size: 18px; }}
                    
                    /* Typography */
                    h1, h2, h3 {{ color: #1E3A5F; }}
                    p {{ margin: 10px 0; }}
                    strong {{ color: #1E3A5F; font-weight: bold; }}
                    
                    /* Footer */
                    .footer {{ text-align: center; margin-top: 30px; padding: 15px; border-top: 1px solid #eee; color: #666; font-size: 12px; }}
                    
                    /* Button */
                    .btn {{ display: inline-block; background-color: #F7931E; color: white; padding: 12px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; margin-top: 20px; text-align: center; }}
                    
                    /* Mobile responsiveness */
                    @media only screen and (max-width: 480px) {{
                        .container {{ width: 100%; border-radius: 0; }}
                        .content {{ padding: 15px; }}
                        .thank-you {{ padding: 15px; }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img_tag}
                        <h1>Thank You for Your Service!</h1>
                    </div>
                    <div class="content">
                        <p>Hi {first_name},</p>
                        
                        <div class="thank-you">
                            <h2>Your Contribution Made a Difference!</h2>
                            <p>We want to express our sincere gratitude for your time and dedication as a volunteer at <strong>{event_name}</strong>. Your selfless service has made a positive impact on our community.</p>
                        </div>
                        
                        <p>Thanks to volunteers like you, we can continue to provide essential services and support to our community. Your willingness to give your time and energy is truly inspiring.</p>
                        
                        <p>We hope to see you at future events. Your continued support is invaluable to us.</p>
                        
                        <p>With gratitude,</p>
                        <p>The Laredo Public Health Team</p>
                    </div>
                    <div class="footer">
                        <p>&copy; {datetime.now().year} Volunteer System - Laredo Public Health</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
            Thank you for your service at {event_name}!
            
            Hi {first_name},
            
            Your Contribution Made a Difference!
            
            We want to express our sincere gratitude for your time and dedication as a volunteer at {event_name}. Your selfless service has made a positive impact on our community.
            
            Thanks to volunteers like you, we can continue to provide essential services and support to our community. Your willingness to give your time and energy is truly inspiring.
            
            We hope to see you at future events. Your continued support is invaluable to us.
            
            With gratitude,
            The Laredo Public Health Team
            
            Volunteer System - Laredo Public Health
            """
        
        # Send the email
        return self.send_email(
            to_email=email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

# Create an instance of EmailService that can be imported elsewhere
email_service = EmailService()
