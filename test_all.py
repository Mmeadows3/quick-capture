"""
test_all.py - Automated test suite for Quick Capture

Tests each module incrementally to ensure everything works before startup.
Runs automatically when you start the program.
"""
import sys
from pathlib import Path

def print_test(name, passed, details=""):
    """Print test result in consistent format"""
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {name}")
    if details:
        print(f"       {details}")
    return passed

def test_step_1_save_note():
    """
    Test Step 1: save_note.py can save to daily.org

    What we're testing:
    - Module imports without errors
    - Can create directory if needed
    - Can write to daily.org
    - Format is correct (* [timestamp] text)
    """
    print("\n[Step 1] Testing save_note.py...")

    try:
        # Import the module
        from save_note import save_note, DAILY_ORG_PATH

        if not print_test("Import save_note module", True):
            return False

        # Test saving a note
        test_text = "Automated test note"
        success = save_note(test_text)

        if not print_test("Save test note", success, f"Writing to {DAILY_ORG_PATH}"):
            return False

        # Verify the file exists
        file_exists = Path(DAILY_ORG_PATH).exists()
        if not print_test("daily.org file exists", file_exists, DAILY_ORG_PATH):
            return False

        # Verify the content format
        with open(DAILY_ORG_PATH, 'r', encoding='utf-8') as f:
            last_line = f.readlines()[-1]

        # Check format: "* [YYYY-MM-DD HH:MM] text"
        is_correct_format = (
            last_line.startswith("* [") and
            "] " in last_line and
            test_text in last_line
        )

        if not print_test("Format is correct", is_correct_format, last_line.strip()):
            return False

        print("[Step 1] All tests passed!\n")
        return True

    except Exception as e:
        print_test("Step 1 tests", False, str(e))
        return False

def test_step_2_capture_window():
    """
    Test Step 2: capture_window.py can be imported

    What we're testing:
    - Module imports without errors
    - PowerShell is available (for Windows Forms GUI)
    - capture_window.ps1 script exists

    Note: We can't automatically test the GUI without user interaction.
    The window will be tested when you use the program.
    """
    print("[Step 2] Testing capture_window.py...")

    try:
        # Check if PowerShell is available
        import subprocess
        result = subprocess.run(['powershell', '-Command', 'Write-Output "OK"'],
                              capture_output=True, text=True, timeout=5)
        if not print_test("PowerShell available", result.returncode == 0, "For Windows Forms GUI"):
            return False

        # Check if PowerShell script exists
        from pathlib import Path
        ps_script = Path(__file__).parent / "capture_window.ps1"
        if not print_test("capture_window.ps1 exists", ps_script.exists(), str(ps_script)):
            return False

        # Import the module
        from capture_window import show_capture_window
        if not print_test("Import capture_window module", True):
            return False

        print("[Step 2] All tests passed!")
        print("       Note: GUI will be tested when you press Ctrl+Left Alt\n")
        return True

    except Exception as e:
        print_test("Step 2 tests", False, str(e))
        return False

def test_step_3_quick_capture():
    """
    Test Step 3: quick_capture.py combines window + save

    What we're testing:
    - Module imports without errors
    - Can access both save_note and capture_window
    """
    print("[Step 3] Testing quick_capture.py...")

    try:
        # Import the module
        from quick_capture import capture_and_save
        if not print_test("Import quick_capture module", True):
            return False

        # Verify it can access the dependencies
        import save_note
        import capture_window

        if not print_test("Dependencies accessible", True, "save_note + capture_window"):
            return False

        print("[Step 3] All tests passed!")
        print("       Note: Full flow tested when you press Ctrl+Left Alt\n")
        return True

    except Exception as e:
        print_test("Step 3 tests", False, str(e))
        return False

def test_step_4_hotkey_listener():
    """
    Test Step 4: hotkey_listener.py can listen for keys

    What we're testing:
    - keyboard library is installed
    - Module imports without errors
    - Can access quick_capture
    """
    print("[Step 4] Testing hotkey_listener.py...")

    try:
        # Import keyboard library
        import keyboard
        if not print_test("keyboard library installed", True):
            return False

        # Import the module
        from hotkey_listener import start_listening, HOTKEY
        if not print_test("Import hotkey_listener module", True):
            return False

        if not print_test("Hotkey configured", True, f"Listening for: {HOTKEY}"):
            return False

        print("[Step 4] All tests passed!\n")
        return True

    except ImportError as e:
        if 'keyboard' in str(e):
            print_test("keyboard library installed", False, "Run: pip install keyboard")
        else:
            print_test("Step 4 tests", False, str(e))
        return False
    except Exception as e:
        print_test("Step 4 tests", False, str(e))
        return False

def run_all_tests():
    """
    Run all tests in order.

    Returns:
        bool: True if all tests pass, False if any fail
    """
    print("=" * 60)
    print("Quick Capture - Automated Test Suite")
    print("=" * 60)
    print()
    print("Running incremental tests...")
    print("Each test builds on the previous one.")

    # Run tests in order (cumulative)
    tests = [
        test_step_1_save_note,
        test_step_2_capture_window,
        test_step_3_quick_capture,
        test_step_4_hotkey_listener
    ]

    for test in tests:
        if not test():
            print()
            print("=" * 60)
            print("[FAILED] Tests failed. Fix errors above before using.")
            print("=" * 60)
            return False

    # All tests passed
    print("=" * 60)
    print("[SUCCESS] All tests passed! Ready to use.")
    print("=" * 60)
    print()
    return True

# Run tests if executed directly
if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
