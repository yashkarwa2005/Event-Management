@echo off
setlocal EnableDelayedExpansion

:: -----------------------------------------------------------------------------
:: One-Click Automated GitHub Project, Issues, Labels & Kanban Board Setup
:: Compatible with any cloned GitHub repository and user account.
:: -----------------------------------------------------------------------------

title GitHub Scrum Project Setup - One-Click Setup

:: Set working directory to project root
cd /d "%~dp0"

echo =====================================================================
echo           ONE-CLICK GITHUB SCRUM PROJECT & KANBAN SETUP
echo =====================================================================
echo.
echo Preparing environment and checking prerequisites...
echo.

:: 1. Check Git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not found in system PATH.
    echo.
    echo WHAT IS MISSING: Git Version Control System
    echo WHY IT IS NEEDED: Required to read repository remote and manage codebase.
    echo HOW TO INSTALL : Download and install from https://git-scm.com/downloads
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

:: 2. Check and locate GitHub CLI (gh)
set "GH_FOUND=0"
where gh >nul 2>nul
if %errorlevel% equ 0 (
    set "GH_FOUND=1"
) else (
    if exist "%LOCALAPPDATA%\GitHubCLI\gh.exe" (
        set "PATH=%LOCALAPPDATA%\GitHubCLI;%PATH%"
        set "GH_FOUND=1"
    ) else if exist "%LOCALAPPDATA%\Programs\GitHub CLI\bin\gh.exe" (
        set "PATH=%LOCALAPPDATA%\Programs\GitHub CLI\bin;%PATH%"
        set "GH_FOUND=1"
    ) else if exist "C:\Program Files\GitHub CLI\gh.exe" (
        set "PATH=C:\Program Files\GitHub CLI;%PATH%"
        set "GH_FOUND=1"
    ) else if exist "C:\Program Files\GitHub CLI\bin\gh.exe" (
        set "PATH=C:\Program Files\GitHub CLI\bin;%PATH%"
        set "GH_FOUND=1"
    )
)

if "%GH_FOUND%"=="0" (
    echo [NOTICE] GitHub CLI ('gh'^) was not detected in PATH.
    echo.
    echo WHAT IS MISSING: GitHub CLI ('gh'^)
    echo WHY IT IS NEEDED: Authenticates securely with your GitHub account,
    echo                   creates Labels, Milestones, Scrum Issues, and
    echo                   configures your GitHub Projects Kanban board.
    echo.
    echo HOW TO INSTALL:
    echo   Option A: Automatic via Windows Package Manager:
    echo             winget install --id GitHub.cli
    echo   Option B: Download installer from:
    echo             https://cli.github.com/
    echo.
    
    where winget >nul 2>nul
    if !errorlevel! equ 0 (
        set /p INSTALL_GH="Would you like to install GitHub CLI automatically via winget right now? [Y/N]: "
        if /i "!INSTALL_GH!"=="Y" (
            echo.
            echo [*] Installing GitHub CLI... Please wait a moment.
            winget install --id GitHub.cli --exact --accept-source-agreements --accept-package-agreements
            where gh >nul 2>nul
            if !errorlevel! equ 0 (
                set "GH_FOUND=1"
                echo [+] GitHub CLI installed successfully!
            ) else (
                echo [!] Please restart this script after the installation finishes.
            )
        )
    )
)

:: 3. Execute setup engine via PowerShell
if exist ".github\setup\setup-project.ps1" (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".github\setup\setup-project.ps1"
    set "SETUP_EXIT=!errorlevel!"
) else if exist ".github\setup\setup_project.py" (
    python .github\setup\setup_project.py
    set "SETUP_EXIT=!errorlevel!"
) else (
    echo [ERROR] Setup script not found in .github\setup\
    set "SETUP_EXIT=1"
)

echo.
if !SETUP_EXIT! equ 0 (
    echo [SUCCESS] GitHub Scrum Project setup finished successfully!
) else (
    echo [NOTICE] Setup finished with code !SETUP_EXIT!. Please review any messages above.
)

echo.
echo Press any key to close this window...
pause >nul
exit /b !SETUP_EXIT!
