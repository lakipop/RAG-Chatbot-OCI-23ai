@echo off
REM ============================================================
REM START CHATBOT APPLICATION
REM ============================================================
REM This script launches the Streamlit chatbot web application.
REM Run this AFTER you have completed the ingestion step.
REM
REM What it does:
REM 1. Activates virtual environment
REM 2. Verifies .env file exists
REM 3. Launches Streamlit app (opens in your default browser)
REM
REM The app will run until you close this window or press Ctrl+C
REM ============================================================

echo.
echo ============================================================
echo   OCI RAG PROJECT - STARTING CHATBOT
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

echo [INFO] Starting Streamlit application...
echo.
echo The chatbot will open in your default web browser.
echo If it doesn't open automatically, go to: http://localhost:8501
echo.
echo ============================================================
echo   CHATBOT IS RUNNING
echo ============================================================
echo.
echo To stop the chatbot:
echo   - Press Ctrl+C in this window, or
echo   - Close this window
echo.
echo ============================================================
echo.

streamlit run main_app.py

echo.
echo ============================================================
echo   CHATBOT STOPPED
echo ============================================================
echo.
pause
