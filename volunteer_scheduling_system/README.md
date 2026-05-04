# Volunteer Scheduling System

A dynamic, modular volunteer scheduling system for the City of Laredo. Admins can create volunteer events from a web-based dashboard, each generating a public-facing sign-up form and an admin dashboard at dynamic URLs.

## Project Structure

The project is organized into two main sections:

- **Public (Volunteer) Section**: Accessible to anyone, contains the volunteer registration forms
- **Admin (Private) Section**: Accessible only to authorized staff, contains event management and volunteer data

### Directory Structure

```
volunteer-platform/
  backend/
    models/       - Database models
    routes/       - API routes (admin_routes.py, volunteer_routes.py, etc.)
    utils/        - Utility functions
    auth.py       - Authentication system
    app.py        - Flask application
    config.py     - Configuration
  frontend/
    static/
      css/        - Stylesheets
      img/        - Images
      js/
        admin/    - Admin JavaScript files
        volunteer/ - Volunteer JavaScript files
    templates/
      admin/      - Admin HTML templates
      volunteer/  - Volunteer HTML templates
      base.html   - Base template
      error.html  - Error page
    data/         - Example data files
```

## Authentication

The system uses a simple username/password authentication system for admin access. Public volunteer forms remain accessible without authentication.

### Admin Login Credentials

To access the admin section, use the following credentials:

- **Username:** `admin`
- **Password:** `password123`

These credentials are defined in the `backend/auth.py` file and can be changed there for production use.

**Note**: These are placeholder credentials for development. In production, use strong passwords and consider integrating with the City of Laredo's authentication system.

### Testing the Application

After starting the application:

1. Access the admin login at: http://localhost:5000/admin/login (or the port you specified)
2. Log in with the credentials above
3. After logging in, you'll be redirected to the admin home page
4. Create events and manage volunteers through the admin interface
5. Access volunteer forms at: http://localhost:5000/volunteer/form/<event_id>

## URL Structure

- **Admin URLs**: `/admin/...`
  - `/admin/` - Admin home page
  - `/admin/login` - Admin login
  - `/admin/dashboard/<event_id>` - Event dashboard

- **Volunteer URLs**: `/volunteer/...`
  - `/volunteer/form/<event_id>` - Volunteer registration form

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas account)

### Installation

#### Automatic Setup (Recommended)

1. Clone the repository
2. Run the setup script:
   - **Windows**: Run `setup.bat`
   - **macOS/Linux**: Run `./setup.sh`

This will create a virtual environment and install all required dependencies.

#### Manual Setup

If the automatic setup doesn't work, you can set up the environment manually:

1. Clone the repository
2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows**: 
     ```
     venv\Scripts\activate
     ```
   - **macOS/Linux**: 
     ```
     source venv/bin/activate
     ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### MongoDB Setup

The application requires a MongoDB database. You have two options:

#### Option 1: Local MongoDB Installation

1. Install MongoDB Community Edition:
   - **Windows**: [MongoDB Windows Installation Guide](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)
   - **macOS**: [MongoDB macOS Installation Guide](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
   - **Linux**: [MongoDB Linux Installation Guide](https://docs.mongodb.com/manual/administration/install-on-linux/)

2. Start MongoDB:
   - **Windows**: Run MongoDB as a service or use `mongod` command
   - **macOS/Linux**: Run `mongod` in terminal

3. The application is already configured to connect to a local MongoDB instance at `mongodb://localhost:27017/volunteer_db`

#### Option 2: MongoDB Atlas (Cloud)

1. Create a free MongoDB Atlas account at [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Get your connection string from Atlas (it will look like `mongodb+srv://username:password@cluster.mongodb.net/volunteer_db`)
4. Update the `.env` file with your MongoDB Atlas connection string:
   ```
   MONGO_URI=your_atlas_connection_string_here
   ```

### Running the Application

1. Start MongoDB (if using local installation):
   - **Windows**: Run `start_mongodb.bat`
   - **macOS/Linux**: Run `./start_mongodb.sh`
   
   Alternatively, you can use MongoDB Compass or run MongoDB as a service.

2. Check MongoDB connection (optional):
   ```
   python check_mongodb.py
   ```
   This script will verify if MongoDB is running and accessible.

3. Start the application:
   ```
   python run.py
   ```
   
4. Open your browser and navigate to `http://localhost:5000`

## Features

- Event creation with custom form fields
- Dynamic form rendering based on JSON configuration
- Volunteer submission management
- Shift-based Excel export
- Receipt-style confirmation for volunteers
- Bilingual support (English/Spanish)
- Secure admin access with authentication

## Security Considerations

- The application uses session-based authentication for admin access
- All admin routes are protected with login requirements
- In production, ensure HTTPS is enabled
- Store sensitive information like SECRET_KEY in environment variables
- Regularly update the admin password

## Deployment on City of Laredo Website

For deployment on the City of Laredo website:

1. Configure the application with appropriate security settings
2. Set up HTTPS
3. Integrate with the city's authentication system if available
4. Consider using a subdomain (e.g., volunteer.cityoflaredo.gov)

## Troubleshooting

### MongoDB Connection Issues

If you encounter MongoDB connection errors:

1. Ensure MongoDB is running (if using local installation)
2. Check your connection string in the `.env` file
3. If using MongoDB Atlas, ensure your IP address is whitelisted in the Atlas dashboard
4. Verify network connectivity to the MongoDB server

### Authentication Issues

If you encounter authentication issues:

1. Check that you're using the correct username and password
2. Ensure the session cookie is being set correctly
3. Verify that the SECRET_KEY is properly configured
