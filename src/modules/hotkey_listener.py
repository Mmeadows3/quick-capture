"""
hotkey_listener.py - Stateless hotkey detection

This module does ONE thing: listens for a hotkey and calls a callback.
NO state - hotkey and callback come from parameters.
Pure infrastructure - no application logic.
"""
import sys
import time
import keyboard
from config import default_config

def start_listening(hotkey=None, on_trigger=None, config=None, quiet=False):
    """
    Start listening for the hotkey and call callback when pressed.

    This is a PURE FUNCTION (mostly):
    - Takes inputs (hotkey, callback, config, quiet flag)
    - No global state (except keyboard library's internal state)

    Args:
        hotkey: Key combination to listen for (e.g., 'ctrl+alt')
                Uses config.hotkey if None
        on_trigger: Function to call when hotkey pressed (REQUIRED)
        config: Configuration object (uses default if None)
        quiet: If True, don't print banner

    How it works:
        1. Registers hotkey with keyboard library
        2. When hotkey pressed, calls on_trigger function
        3. Keeps running until Ctrl+C is pressed

    Why this design?
        - Testable: can pass different hotkeys and callbacks
        - Flexible: can use for different purposes, not just capture
        - No global state: everything comes from parameters
        - Pure infrastructure: no application logic
    """
    # Use defaults if not provided
    if config is None:
        config = default_config

    if hotkey is None:
        hotkey = config.hotkey

    if on_trigger is None:
        raise ValueError("on_trigger callback is required")

    # Only print banner if not quiet
    if not quiet:
        print("=" * 60)
        print("Quick Capture")
        print("=" * 60)
        print(f"Press {hotkey.upper()} to capture | Ctrl+C to exit")
        print("=" * 60)

    # Small delay to ensure clean startup
    time.sleep(0.3)

    # Track activation time to prevent phantom triggers
    # The keyboard library sometimes triggers immediately after registration
    activation_time = time.time()
    cooldown_seconds = 1.0  # Ignore triggers in first second

    # Track last trigger to prevent double-firing
    last_trigger_time = 0
    min_interval = 0.5  # Minimum 500ms between captures

    def debounced_trigger():
        """Wrapper that ignores immediate phantom triggers and double-fires"""
        nonlocal last_trigger_time

        current_time = time.time()
        elapsed_since_start = current_time - activation_time
        elapsed_since_last = current_time - last_trigger_time

        # Ignore phantom triggers during initial cooldown
        if elapsed_since_start < cooldown_seconds:
            return

        # Ignore if triggered too soon after last capture
        if last_trigger_time > 0 and elapsed_since_last < min_interval:
            print(f"Ignoring double-trigger ({elapsed_since_last:.2f}s since last)")
            return

        last_trigger_time = current_time
        on_trigger()

    # Register the hotkey with debounced wrapper
    # hotkey string tells keyboard library which keys to watch for
    # When both keys pressed together → debounced_trigger() is called
    # Goal: Trigger capture anywhere, anytime with one key combo
    keyboard.add_hotkey(hotkey, debounced_trigger)

    # Keep the program running
    # keyboard.wait() blocks (doesn't return) until interrupted
    # try/except catches Ctrl+C interrupt for clean shutdown
    # Goal: Run forever, listening for hotkey, until user exits
    try:
        keyboard.wait()  # Wait forever (until Ctrl+C)
    except KeyboardInterrupt:
        # KeyboardInterrupt = exception raised when user presses Ctrl+C
        # '\n\n' = two newlines for visual spacing
        print("\n\n[EXIT] Shutting down...")

# Note: Cannot run standalone - needs a callback
# Use main.py as the entry point instead
