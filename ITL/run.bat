@echo off
title EventSphere - Event Management System (ITL Lab & Scrum PBL)
color 0a
echo ===============================================================================
echo   🎪 EVENTSPHERE : EVENT MANAGEMENT SYSTEM (ITL LAB & SCRUM PBL)
echo   Author: Sangram Shinde (B.Tech 3rd Year)
echo   Subject: Information Technology Lab (ITL) & Agile Methodologies (AM)
echo ===============================================================================
echo.
echo Starting EventSphere Web Server and Interactive Dashboard...
echo Database: SQLite (database/event.db)
echo Concurrency Guard: Atomic Transactions Enabled (Zero Overbooking)
echo.

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not found in system PATH!
    echo Please install Python 3.10+ from python.org and tick 'Add Python to PATH'.
    pause
    exit /b 1
)

python app.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo Server exited with an error. Press any key to close.
    pause
)
