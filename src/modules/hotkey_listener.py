"""
System-wide keyboard hotkey listener.

Monitors for a specific key combination (e.g., Ctrl+Alt) and triggers
a callback when pressed. Works from any app.
"""
import time
import keyboard

def start_listening(hotkey, on_trigger, config, quiet=False):
    """
    Listen for system-wide hotkey, call callback when pressed.

    Includes debouncing to filter out:
    - Phantom triggers (keyboard library quirk on registration)
    - Double-triggers (user holding keys too long)

    Args:
        hotkey: Key combination string (e.g., 'ctrl+alt')
        on_trigger: Function to call when hotkey pressed
        config: Config object (for display only)
        quiet: Skip startup banner if True
    """
    if not quiet:
        print("=" * 60)
        print("Quick Capture")
        print("=" * 60)
        print(f"Press {hotkey.upper()} to capture | Ctrl+C to exit")
        print("=" * 60)

    # Small startup delay to prevent phantom triggers
    time.sleep(0.3)

    # Debounce timing
    activation_time = time.time()
    cooldown_seconds = 1.0  # Ignore triggers in first second
    last_trigger_time = 0
    min_interval = 0.5  # Minimum 500ms between captures

    def debounced_trigger():
        """Wrapper that filters phantom and double triggers."""
        nonlocal last_trigger_time

        current_time = time.time()
        elapsed_since_start = current_time - activation_time
        elapsed_since_last = current_time - last_trigger_time

        # Skip phantom triggers during startup cooldown
        if elapsed_since_start < cooldown_seconds:
            return

        # Skip rapid double-triggers (user holding keys)
        if last_trigger_time > 0 and elapsed_since_last < min_interval:
            print(f"Ignoring double-trigger ({elapsed_since_last:.2f}s since last)")
            return

        last_trigger_time = current_time
        on_trigger()

    # Register system-wide hotkey
    keyboard.add_hotkey(hotkey, debounced_trigger)

    # Run until Ctrl+C
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("\n\n[EXIT] Shutting down...")
