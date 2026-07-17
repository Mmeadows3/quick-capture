@echo off
echo.
echo Quick Capture - Starting...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    pause
    exit /b 1
)

REM Install keyboard library if needed
pip show keyboard >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -q keyboard >nul 2>&1
)

REM Add src to Python path so imports work
set PYTHONPATH=%CD%\src;%PYTHONPATH%

REM Run health checks
echo Running health checks...
python tests\test_runner.py --quiet
if errorlevel 1 (
    echo.
    echo Health checks failed. Fix errors above.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Quick Capture Ready
echo ============================================================
echo Press Ctrl+Left Alt to capture notes
echo Press Ctrl+C to exit
echo ============================================================
echo.

REM Start listener (silently)
python src\main.py
