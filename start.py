"""
Voice Input Launcher
====================
Single script to test and start the voice input system.

Usage: python start.py [--skip-tests]
"""
import subprocess
import sys
from pathlib import Path
import time

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def run_tests():
    """Run automated tests"""
    print_header("RUNNING TESTS")

    test_script = Path(__file__).parent / "tests" / "test_simplified.py"

    print("\nRunning simplified test suite...")
    print("(1) Voice-to-text capture")
    print("(2) File writing to daily.org\n")

    try:
        result = subprocess.run(
            [sys.executable, str(test_script)],
            capture_output=False,
            text=True
        )

        if result.returncode == 0:
            print("\n[SUCCESS] All tests passed!")
            return True
        else:
            print("\n[WARNING] Some tests failed, but continuing anyway...")
            return True  # Continue even if tests fail
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        return False

def start_ahk():
    """Start AutoHotkey script"""
    print_header("STARTING AUTOHOTKEY")

    ahk_script = Path(__file__).parent / "voice_to_file.ahk"

    if not ahk_script.exists():
        print(f"\n[ERROR] AutoHotkey script not found: {ahk_script}")
        print("Please ensure voice_to_file.ahk is in the voice_input directory.")
        return False

    print(f"\nStarting: {ahk_script}")
    print("\nHotkey: Ctrl + Left Alt (toggle)")
    print("Press Ctrl + Left Alt to start/stop voice dictation")
    print("\nAutoHotkey is now running in the background.")
    print("Close this window or press Ctrl+C to stop.\n")

    try:
        # Start AHK script
        process = subprocess.Popen(
            [str(ahk_script)],
            shell=True
        )

        print("[SUCCESS] Voice input system is running!")
        print("\nUsage:")
        print("  1. Press Ctrl + Left Alt to START dictation")
        print("  2. Speak your text")
        print("  3. Press Ctrl + Left Alt again to STOP (or wait 5s after stopping)")
        print("  4. Text appears in daily.org as a bullet point")

        # Keep the script running
        print("\n" + "-"*70)
        print("Press Ctrl+C to stop the system")
        print("-"*70 + "\n")

        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n\nStopping voice input system...")
            process.terminate()
            print("[STOPPED] Voice input system stopped.")

        return True

    except Exception as e:
        print(f"\n[ERROR] Failed to start AutoHotkey: {e}")
        print("\nMake sure AutoHotkey v2.0 is installed:")
        print("  https://www.autohotkey.com/")
        return False

def main():
    print_header("VOICE INPUT SYSTEM LAUNCHER")

    print("\nThis will:")
    print("  1. Run tests to verify the system works")
    print("  2. Start the AutoHotkey hotkey listener")
    print("  3. Enable Ctrl + Left Alt voice input")

    # Check for skip-tests flag
    skip_tests = "--skip-tests" in sys.argv

    if not skip_tests:
        input("\nPress ENTER to run tests...")
        if not run_tests():
            print("\n[ERROR] Tests failed. Fix issues before starting.")
            return 1

        time.sleep(1)
    else:
        print("\n[SKIPPED] Tests skipped (--skip-tests flag)")

    input("\nPress ENTER to start the voice input system...")

    if not start_ahk():
        print("\n[ERROR] Failed to start system.")
        return 1

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Startup cancelled by user.")
        sys.exit(0)
