# backend/auth.py

import os
from functools import wraps
from flask import session, redirect, url_for, request, flash

# In a real application, this would be stored in a database
# For now, we'll use a simple dictionary with username and password
# The password should be hashed in a real application
ADMIN_USERS = {
    "admin": "password123"  # This is just a placeholder - would be hashed in production
}

def login_required(f):
    """
    Decorator to require login for routes.
    
    Args:
        f: The function to decorate
        
    Returns:
        function: The decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            # Store the requested URL for redirecting after login
            session['next_url'] = request.url
            return redirect(url_for('admin_routes.login'))
        return f(*args, **kwargs)
    return decorated_function

def authenticate_user(username, password):
    """
    Authenticate a user with username and password.
    
    Args:
        username (str): The username
        password (str): The password
        
    Returns:
        bool: True if authentication is successful, False otherwise
    """
    # In a real application, you would hash the password and compare with the stored hash
    if username in ADMIN_USERS and ADMIN_USERS[username] == password:
        return True
    return False
