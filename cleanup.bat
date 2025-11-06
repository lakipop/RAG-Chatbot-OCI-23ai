@echo off
REM ============================================================
REM CLEANUP SCRIPT
REM ============================================================
REM This script removes the virtual environment and generated files.
REM Use this if you want to start fresh or if something went wrong
REM during setup.
REM
REM What it removes:
REM - venv/ folder (virtual environment)
REM - __pycache__/ folders (Python cache)
REM - .pyc files (compiled Python files)
REM
REM What it KEEPS:
REM - .env file (your credentials)
REM - data/ folder (your documents)
REM - All source code files
REM
REM After running this, you'll need to run setup.bat again.
REM ============================================================

echo.
echo ============================================================
echo   OCI RAG PROJECT - CLEANUP
echo ============================================================
echo.
echo [WARNING] This will delete:
echo   - venv/ folder (virtual environment)
echo   - All __pycache__/ folders
echo   - All .pyc files
echo.
echo Your .env file and data/ folder will be preserved.
echo.

set /p confirm="Are you sure you want to continue? (y/n): "
if /i not "%confirm%"=="y" (
    echo.
    echo Cleanup cancelled.
    pause
    exit /b 0
)

echo.
echo Starting cleanup...
echo.

REM Remove virtual environment
if exist "venv\" (
    echo [1/3] Removing virtual environment...
    rmdir /s /q venv
    echo Virtual environment removed.
) else (
    echo [1/3] Virtual environment not found (already clean).
)
echo.

REM Remove __pycache__ directories
echo [2/3] Removing Python cache folders...
for /d /r %%d in (__pycache__) do (
    if exist "%%d" (
        rmdir /s /q "%%d"
        echo   Removed: %%d
    )
)
echo.

REM Remove .pyc files
echo [3/3] Removing compiled Python files...
del /s /q *.pyc >nul 2>&1
echo.

echo ============================================================
echo   CLEANUP COMPLETE!
echo ============================================================
echo.
echo Your project has been cleaned.
echo To use the project again, run: setup.bat
echo.
pause
