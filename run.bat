@echo off
title EventSphere - Event Management System (AM Scrum PBL)
color 0a
echo ===============================================================================
echo   🎪 EVENTSPHERE : EVENT MANAGEMENT SYSTEM
echo   B.Tech 3rd Year Agile Methodology PBL Project
echo   Lead: Sangram Shinde
echo ===============================================================================
echo.
echo Starting EventSphere Web Server and Dashboard...
echo Database: SQLite (database/event.db)
echo Concurrency Guard: Atomic Transactions Enabled
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
