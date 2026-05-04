@echo off
REM Simple script to start MongoDB on Windows

echo Starting MongoDB...

REM Check if MongoDB is installed
where mongod >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo MongoDB (mongod) not found in PATH.
    echo Please make sure MongoDB is installed correctly.
    echo.
    echo Installation guide:
    echo - Download and install MongoDB Community Edition from:
    echo   https://www.mongodb.com/try/download/community
    echo - Or use MongoDB Compass which includes MongoDB:
    echo   https://www.mongodb.com/products/compass
    echo.
    echo After installing, try running this script again.
    echo.
    echo Alternatively, you can use MongoDB Atlas cloud service.
    echo Update the MONGO_URI in the .env file to use MongoDB Atlas.
    exit /b 1
)

REM Create data directory if it doesn't exist
if not exist data\db (
    echo Creating data directory...
    mkdir data\db
)

REM Start MongoDB
echo Starting MongoDB server...
start "MongoDB" mongod --dbpath=data\db

echo MongoDB server started in a new window.
echo Press any key to close this window...
pause >nul
