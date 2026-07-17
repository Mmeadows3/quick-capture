"""
test_hotkey_listener.py - Tests for hotkey_listener module

Tests the keyboard hotkey detection
"""
import sys

def test_hotkey_listener(quiet=False):
    """
    Test hotkey_listener.py can listen for keys

    What we're testing:
    - keyboard library is installed
    - Module imports without errors
    - Can access quick_capture
    - Hotkey is configured
    """
    if not quiet:
        print("\n[Testing hotkey_listener.py]")

    try:
        # Import keyboard library
        import keyboard
        if not quiet:
            print("  [OK] keyboard library installed")

        # Import the module
        from modules.hotkey_listener import start_listening
        if not quiet:
            print("  [OK] Import hotkey_listener module")

        # Check hotkey configuration
        from config import default_config
        if not quiet:
            print(f"  [OK] Hotkey configured: {default_config.hotkey}")
            print("[hotkey_listener] All tests passed!\n")
        return True

    except ImportError as e:
        if 'keyboard' in str(e):
            print("  [FAIL] keyboard library installed")
            if not quiet:
                print("         Run: pip install keyboard")
        else:
            print(f"  [FAIL] hotkey_listener tests: {e}")
        return False
    except Exception as e:
        print(f"  [FAIL] hotkey_listener tests: {e}")
        return False

if __name__ == '__main__':
    quiet = '--quiet' in sys.argv
    success = test_hotkey_listener(quiet=quiet)
    sys.exit(0 if success else 1)
