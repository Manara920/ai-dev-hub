@echo off
REM ==============================================================================
REM  Al-Manara AI Dev Hub Pro - Windows Auto Installer
REM ==============================================================================

cd /d "%~dp0"

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
if %errorlevel% neq 0 (
    echo [-] Warning: Failed to upgrade pip. Continuing with installation...
)

python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [-] Error: Failed to install Python dependencies from requirements.txt.
    pause
    exit /b %errorlevel%
)

REM Create .env from template if missing
if not exist "config\.env" (
    if exist "config\.env.example" (
        copy config\.env.example config\.env >nul
        echo [+] Created config\.env template
    )
)

REM Generate Windows command wrappers for groq CLI
echo [*] Generating Windows command wrappers for groq...
(
echo @echo off
echo python "%%~dp0bin\groq" %%*
) > "%~dp0groq.cmd"

(
echo @echo off
echo python "%%~dp0groq" %%*
) > "%~dp0bin\groq.bat"

echo [+] Created groq.cmd and bin\groq.bat

echo.
echo ==========================================================
echo  [✓] Setup completed successfully!
echo  To run the application anytime, type:
echo    python ai_hub.py
echo  To run the Groq CLI directly:
echo    groq --help
echo ==========================================================
pause
