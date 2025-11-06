@echo off
REM ============================================================
REM INITIAL SETUP SCRIPT FOR OCI RAG PROJECT
REM ============================================================
REM This script automates the initial setup of the project.
REM Run this ONCE when you first clone the repository.
REM
REM What it does:
REM 1. Creates Python virtual environment
REM 2. Activates the virtual environment
REM 3. Upgrades pip to latest version
REM 4. Installs all Python dependencies
REM 5. Creates .env file from template
REM
REM After running this, you need to:
REM - Edit .env file with your credentials
REM - Run run_ingestion.bat to load your documents
REM - Run start_chatbot.bat to launch the app
REM ============================================================

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo.
echo ============================================================
echo   OCI RAG PROJECT - INITIAL SETUP
echo ============================================================
echo.
echo Working directory: %CD%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.11+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version
echo.

REM Check if virtual environment already exists
if exist "venv\" (
    echo [WARNING] Virtual environment already exists!
    echo If you want to recreate it, delete the 'venv' folder first.
    echo.
    REM Use CHOICE for a more robust single-key prompt that works
    REM correctly when run from various terminals (cmd.exe, PowerShell,
    REM or when launched by other programs). CHOICE returns an errorlevel
    REM corresponding to the key pressed (1 = first choice, 2 = second).
    choice /c YN /m "Do you want to continue anyway? (Y/N)"
    REM If user chose 'N' (errorlevel 2) then cancel setup
    if errorlevel 2 (
        echo Setup cancelled.
        pause
        exit /b 0
    )
    echo.
) else (
    echo [2/5] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
    echo.
)

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo Virtual environment activated.
echo.

echo [4/5] Upgrading pip to latest version...
python -m pip install --upgrade pip
echo.

echo [5/5] Installing Python dependencies...
echo This may take 2-3 minutes...
echo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)
echo.

echo [6/6] Creating .env file from template...
if exist ".env" (
    echo [WARNING] .env file already exists!
    echo Skipping to avoid overwriting your credentials.
) else (
    copy .env.example .env >nul
    echo .env file created successfully.
    echo.
    echo ============================================================
    echo   IMPORTANT: EDIT YOUR .env FILE NOW!
    echo ============================================================
    echo.
    echo Before you can run the application, you MUST edit the .env
    echo file with your actual OCI and Oracle Database credentials.
    echo.
    echo The .env file has been created in this directory.
    echo Open it with any text editor and fill in your credentials.
    echo.
)

echo.
echo ============================================================
echo   SETUP COMPLETE!
echo ============================================================
echo.
echo Next steps:
echo   1. Edit the .env file with your credentials
echo   2. Run: run_ingestion.bat (to load documents - ONE TIME ONLY)
echo   3. Run: start_chatbot.bat (to launch the chatbot app)
echo.
echo For quick access, you can also use:
echo   - quick_start.bat (runs ingestion + starts chatbot)
echo.
pause
