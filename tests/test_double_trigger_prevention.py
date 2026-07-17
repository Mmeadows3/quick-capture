"""
test_double_trigger_prevention.py - Ensures hotkey doesn't launch multiple windows

Tests that when a hotkey is pressed, only ONE capture window appears, even if:
- The hotkey is pressed multiple times rapidly
- A capture is already in progress
"""
import sys
import time
import threading
from unittest.mock import Mock, patch

def test_prevents_double_launch(quiet=False):
    """
    Test that only one capture window is launched at a time.

    Scenario: User presses hotkey, window opens. If hotkey pressed again
    before window closes, second window should be blocked.
    """
    if not quiet:
        print("\n[Testing double-launch prevention]")

    from modules.hotkey_listener import start_listening

    # Mock the trigger callback to simulate window being open
    trigger_count = 0
    trigger_times = []
    trigger_lock = threading.Lock()

    def mock_trigger():
        nonlocal trigger_count
        with trigger_lock:
            trigger_count += 1
            trigger_times.append(time.time())
        # Simulate window staying open for 0.5 seconds
        time.sleep(0.5)
        return True

    # Simulate rapid double-press of hotkey
    with patch('keyboard.add_hotkey') as mock_add_hotkey:
        with patch('keyboard.wait'):
            # Start listener
            from config import Config
            config = Config()
            start_listening(
                hotkey=config.hotkey,
                on_trigger=mock_trigger,
                config=config,
                quiet=True
            )

            # Get the registered callback
            registered_callback = mock_add_hotkey.call_args[0][1]

            # Wait for startup cooldown to expire (1.0s)
            time.sleep(1.1)

            # Simulate double-press using threads (concurrent triggers)
            thread1 = threading.Thread(target=registered_callback)
            thread2 = threading.Thread(target=registered_callback)

            thread1.start()
            time.sleep(0.05)  # Small gap to ensure second comes during first
            thread2.start()

            # Wait for both to complete
            thread1.join()
            thread2.join()

            # Verify only ONE trigger went through
            if trigger_count == 1:
                if not quiet:
                    print("  [OK] Double-trigger blocked (only 1 window launched)")
                return True
            else:
                if not quiet:
                    print(f"  [FAIL] Expected 1 launch, got {trigger_count}")
                    print(f"        Trigger times: {trigger_times}")
                return False

def test_allows_sequential_captures(quiet=False):
    """
    Test that captures CAN happen sequentially after sufficient delay.

    Scenario: User captures note, window closes. After 0.5s+, pressing
    hotkey again should work (not permanently blocked).
    """
    if not quiet:
        print("\n[Testing sequential captures allowed]")

    from modules.hotkey_listener import start_listening

    trigger_count = 0

    def mock_trigger():
        nonlocal trigger_count
        trigger_count += 1
        return True

    with patch('keyboard.add_hotkey') as mock_add_hotkey:
        with patch('keyboard.wait'):
            from config import Config
            config = Config()
            start_listening(
                hotkey=config.hotkey,
                on_trigger=mock_trigger,
                config=config,
                quiet=True
            )

            registered_callback = mock_add_hotkey.call_args[0][1]

            # Wait for startup cooldown (1.0s)
            time.sleep(1.1)

            # First capture
            registered_callback()

            # Wait for cooldown to expire (0.5s minimum interval)
            time.sleep(0.6)

            # Second capture (should work)
            registered_callback()

            # Both should have gone through
            if trigger_count == 2:
                if not quiet:
                    print("  [OK] Sequential captures work (got 2 launches)")
                return True
            else:
                if not quiet:
                    print(f"  [FAIL] Expected 2 launches, got {trigger_count}")
                return False

if __name__ == '__main__':
    success1 = test_prevents_double_launch()
    success2 = test_allows_sequential_captures()

    if success1 and success2:
        print("\n[double_trigger_prevention] All tests passed!\n")
        sys.exit(0)
    else:
        print("\n[double_trigger_prevention] Tests failed!\n")
        sys.exit(1)
