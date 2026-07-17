@echo off
REM Quick Capture launcher - handles dependencies, health checks, and startup

echo.
echo Quick Capture - Starting...
echo.

REM Verify Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    pause
    exit /b 1
)

REM Auto-install keyboard library if missing
pip show keyboard >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -q keyboard
)

REM Add src to Python import path
set PYTHONPATH=%CD%\src;%PYTHONPATH%

REM Run health checks (catch issues before user triggers hotkey)
echo Running health checks...
python tests\test_runner.py --quiet
if errorlevel 1 (
    echo.
    echo Health checks failed. Fix errors above.
    pause
    exit /b 1
)

REM Show usage instructions
echo.
echo ============================================================
echo Quick Capture Ready
echo ============================================================
echo Press Ctrl+Left Alt to capture notes
echo Press Ctrl+C to exit
echo ============================================================
echo.

REM Start the listener (runs until Ctrl+C)
python src\main.py
