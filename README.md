# Volunteer Scheduling System

Author: Alexander Ayala

---

## Overview

This project is a full-stack volunteer scheduling system developed in collaboration with a team for a Software Engineering course in partnership with the City of Laredo.

The system provides a centralized platform for managing volunteer events, allowing administrators to create and manage events while enabling volunteers to register for available shifts through a web-based interface.

---

## Project Attribution

This project was developed as part of a team of five students. The original repository is private. This version is included as part of my portfolio to demonstrate my contributions and the system architecture.

My contributions included backend development, REST API design, database integration, and implementation of scheduling and automation features.

---

## Features

- Event creation and management  
- Volunteer registration and shift selection  
- Admin dashboard for managing events and participants  
- Dynamic form system for event-specific inputs  
- RESTful API endpoints for data handling  
- Authentication and session management  
- Automated email notifications  
- Calendar integration (iCalendar and Google Calendar)  
- Excel export for volunteer data  

---

## Technologies Used

- Python  
- Flask  
- MongoDB (PyMongo)  
- HTML, CSS, JavaScript  
- Jinja2  
- REST APIs  

---

## System Architecture

The application is divided into two main components:

- Admin Section – Used for authentication, event creation, and management  
- Volunteer Section – Public interface for browsing events and registering  

The backend is structured using modular Flask Blueprints to separate functionality:

- Admin routes (authentication and dashboard)  
- Event routes (event management)  
- Form routes (dynamic form handling)  
- Volunteer routes (registration and data submission)  

MongoDB is used to store event data, volunteer submissions, and form configurations.

---

## How to Run

1. Install dependencies:
pip install -r requirements.txt

2. Start MongoDB (local or Atlas)

3. Run the application:
python run.py

4. Open in browser:
http://localhost:5000

---

## Notes

- This project was developed for a real stakeholder and presented to City of Laredo representatives  
- Some environment configuration (such as database connection) may be required to run locally  
- Credentials and sensitive data are not included in this repository  

---

## Summary

This project demonstrates full-stack web development, backend architecture design, database-driven systems, and real-world application development for a client-based scenario.
