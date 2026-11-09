@echo off
REM ==============================================================================
REM  Al-Manara AI Dev Hub Pro - Windows Auto Installer
REM ==============================================================================

echo ==========================================================
echo  🏮 Al-Manara AI Dev Hub Pro - Setup for Windows
echo ==========================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [-] Error: Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [*] Upgrading pip and installing requirements...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Create .env from template if missing
if not exist "config\.env" (
    if exist "config\.env.example" (
        copy config\.env.example config\.env >nul
        echo [+] Created config\.env template
    )
)

echo.
echo ==========================================================
echo  [✓] Setup completed successfully!
echo  To run the application anytime, type:
echo  python ai_hub.py
echo ==========================================================
pause
