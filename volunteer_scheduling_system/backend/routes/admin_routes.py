# backend/routes/admin_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from backend.auth import login_required, authenticate_user

admin_bp = Blueprint("admin_routes", __name__, url_prefix="/admin")

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle admin login.
    
    Returns:
        str: Rendered HTML template or redirect
    """
    error = None
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if authenticate_user(username, password):
            session["user"] = username
            next_url = session.pop("next_url", url_for("admin_routes.admin_home"))
            return redirect(next_url)
        else:
            error = "Invalid username or password"
    
    return render_template("admin/login.html", error=error)

@admin_bp.route("/logout")
def logout():
    """
    Handle admin logout.
    
    Returns:
        redirect: Redirect to login page
    """
    session.pop("user", None)
    return redirect(url_for("admin_routes.login"))

@admin_bp.route("/")
@login_required
def admin_home():
    """
    Render the admin home page.
    
    Returns:
        str: Rendered HTML template
    """
    return render_template("admin/admin_home.html")

@admin_bp.route("/dashboard/<event_id>")
@login_required
def event_dashboard(event_id):
    """
    Render the event dashboard for a specific event.
    
    Args:
        event_id (str): The ID of the event
        
    Returns:
        str: Rendered HTML template
    """
    return render_template("admin/event_dashboard.html", event_id=event_id)
