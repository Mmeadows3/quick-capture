"""
test_runner.py - Main test orchestrator

Runs all module tests and presents results.
Usage:
    python test_runner.py          # Verbose output
    python test_runner.py --quiet  # Only show summary
"""
import sys

# Check if quiet mode
QUIET = '--quiet' in sys.argv

def run_all_tests():
    """
    Run all module tests in order.

    Returns:
        bool: True if all tests pass, False if any fail
    """
    if not QUIET:
        print("=" * 60)
        print("Quick Capture - Test Suite")
        print("=" * 60)
        print()
        print("Running module tests...")

    # Import test functions
    from test_save_note import test_save_note
    from test_capture_window import test_capture_window
    from test_hotkey_listener import test_hotkey_listener

    # Run tests in order (cumulative dependencies)
    tests = [
        ("save_note", test_save_note),
        ("capture_window", test_capture_window),
        ("hotkey_listener", test_hotkey_listener)
    ]

    failed = []
    for name, test_func in tests:
        try:
            if not test_func(quiet=QUIET):
                failed.append(name)
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            failed.append(name)

    # Report results
    if failed:
        if QUIET:
            print("  [FAIL] Health checks failed")
        else:
            print()
            print("=" * 60)
            print(f"[FAILED] {len(failed)} test(s) failed: {', '.join(failed)}")
            print("=" * 60)
        return False

    # All tests passed
    if not QUIET:
        print("=" * 60)
        print("[SUCCESS] All tests passed! Ready to use.")
        print("=" * 60)
        print()
    return True

# Run tests if executed directly
if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
