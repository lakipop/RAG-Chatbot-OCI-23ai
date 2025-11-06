@echo off
REM ============================================================
REM DATA INGESTION SCRIPT
REM ============================================================
REM This script runs the data ingestion process.
REM Run this ONCE after initial setup, or whenever you add new
REM documents to the /data folder.
REM
REM What it does:
REM 1. Activates virtual environment
REM 2. Verifies .env file exists
REM 3. Runs ingest.py to load documents into Oracle Vector DB
REM
REM This process may take 30-60 seconds depending on the number
REM of documents you have.
REM ============================================================

echo.
echo ============================================================
echo   OCI RAG PROJECT - DATA INGESTION
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first to set up the project.
    echo.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo.
    echo Please create a .env file with your credentials:
    echo   1. Copy .env.example to .env
    echo   2. Edit .env and fill in your OCI and Oracle DB credentials
    echo.
    echo You can also run setup.bat to create the .env file automatically.
    echo.
    pause
    exit /b 1
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [INFO] Starting data ingestion...
echo This will read documents from the /data folder and store them
echo in your Oracle 23ai Vector Database.
echo.
echo Please wait... (this may take 30-60 seconds)
echo.
echo ============================================================
echo.

python ingest.py

if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo [ERROR] Ingestion failed!
    echo ============================================================
    echo.
    echo Please check the error messages above.
    echo.
    echo Common issues:
    echo   1. Invalid credentials in .env file
    echo   2. Cannot connect to Oracle Database (check network/firewall)
    echo   3. No documents in /data folder
    echo   4. Invalid OCI permissions or quota limits
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   INGESTION COMPLETE!
echo ============================================================
echo.
echo Your documents have been successfully loaded into the database.
echo You can now run the chatbot with: start_chatbot.bat
echo.
pause
