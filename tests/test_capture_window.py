"""
test_capture_window.py - Tests for capture_window module

Tests the PowerShell GUI window functionality
"""
import sys
from pathlib import Path

def test_capture_window(quiet=False):
    """
    Test capture_window.py can be imported

    What we're testing:
    - PowerShell is available (for Windows Forms GUI)
    - capture_window.ps1 script exists
    - Module imports without errors

    Note: We can't automatically test the GUI without user interaction.
    """
    if not quiet:
        print("\n[Testing capture_window.py]")

    try:
        # Check if PowerShell is available
        import subprocess
        result = subprocess.run(['powershell', '-Command', 'Write-Output "OK"'],
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode != 0:
            print(f"  [FAIL] PowerShell available")
            return False
        if not quiet:
            print("  [OK] PowerShell available")

        # Check if PowerShell script exists
        project_root = Path(__file__).parent.parent
        ps_script = project_root / "gui" / "capture_window.ps1"
        
        if not ps_script.exists():
            print(f"  [FAIL] capture_window.ps1 exists")
            if not quiet:
                print(f"       {ps_script}")
            return False
        if not quiet:
            print(f"  [OK] capture_window.ps1 exists")

        # Import the module
        from modules.capture_window import show_capture_window
        if not quiet:
            print("  [OK] Import capture_window module")

        if not quiet:
            print("[capture_window] All tests passed!")
            print("       Note: GUI will be tested when you press hotkey\n")
        return True

    except Exception as e:
        print(f"  [FAIL] capture_window tests: {e}")
        return False

if __name__ == '__main__':
    quiet = '--quiet' in sys.argv
    success = test_capture_window(quiet=quiet)
    sys.exit(0 if success else 1)
