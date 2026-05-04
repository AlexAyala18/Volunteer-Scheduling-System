@echo off
REM Setup script for the Volunteer Scheduling System
REM This script creates a virtual environment and installs dependencies

echo Setting up Volunteer Scheduling System...

REM Check if Python 3 is installed
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH. Please install Python 3 and try again.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment. Please check your Python installation.
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies.
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
echo To start the application:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Start MongoDB (if using local installation):
echo    start_mongodb.bat
echo.
echo 3. Run the application:
echo    python run.py
echo.
echo For more information, see README.md

pause
