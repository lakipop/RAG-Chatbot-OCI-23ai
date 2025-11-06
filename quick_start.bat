@echo off
REM ============================================================
REM QUICK START SCRIPT (INGESTION + CHATBOT)
REM ============================================================
REM This script combines ingestion and chatbot launch in one go.
REM Use this for a fresh start or when you've added new documents.
REM
REM What it does:
REM 1. Activates virtual environment
REM 2. Runs data ingestion (loads documents)
REM 3. If successful, launches the chatbot automatically
REM
REM IMPORTANT: This will re-run ingestion, which clears and
REM reloads all documents. Only use this if you want to
REM refresh your document database.
REM ============================================================

echo.
echo ============================================================
echo   OCI RAG PROJECT - QUICK START
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
    pause
    exit /b 1
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo ============================================================
echo   STEP 1: DATA INGESTION
echo ============================================================
echo.
echo Running data ingestion...
echo This will load all documents from /data folder into the database.
echo.

python ingest.py

if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo [ERROR] Ingestion failed!
    echo ============================================================
    echo.
    echo The chatbot will not start because ingestion failed.
    echo Please fix the errors above and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   STEP 2: STARTING CHATBOT
echo ============================================================
echo.
echo Ingestion successful! Now launching the chatbot...
echo.
echo The chatbot will open in your default web browser.
echo If it doesn't open automatically, go to: http://localhost:8501
echo.
echo To stop the chatbot, press Ctrl+C or close this window.
echo.
echo ============================================================
echo.

streamlit run main_app.py

echo.
echo ============================================================
echo   SESSION ENDED
echo ============================================================
echo.
pause
