@echo off
echo.
echo Quick Capture - Starting...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python not found
    pause
    exit /b 1
)
echo [OK] Python installed

REM Install keyboard library if needed
echo [OK] Checking dependencies...
pip show keyboard >nul 2>&1
if errorlevel 1 (
    echo      Installing keyboard library...
    pip install -q keyboard
)
echo [OK] Dependencies ready

echo.

REM Run automated tests
python test_all.py
if errorlevel 1 (
    echo.
    echo Tests failed. Please fix errors before continuing.
    pause
    exit /b 1
)

echo Starting hotkey listener...
echo.

REM Run the hotkey listener
python hotkey_listener.py
