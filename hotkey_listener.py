"""
hotkey_listener.py - Listens for Ctrl+Left Alt and triggers capture

This module does ONE thing: waits for Ctrl+Left Alt key press, then runs capture.
"""
import keyboard
from quick_capture import capture_and_save

HOTKEY = 'ctrl+alt'  # Ctrl + Left Alt

def start_listening():
    """
    Start listening for the hotkey.

    How it works:
        1. Registers Ctrl+Left Alt as the hotkey
        2. When Ctrl+Left Alt is pressed, calls capture_and_save()
        3. Keeps running until Ctrl+C is pressed

    Why Ctrl+Left Alt?
        - Same as original quick capture project
        - Easy to press with left hand
        - Not commonly used by other apps
    """
    print("=" * 60)
    print("Quick Capture - Hotkey Listener")
    print("=" * 60)
    print()
    print("Press Ctrl+Left Alt to capture a note")
    print("Press Ctrl+C to exit")
    print()
    print("=" * 60)
    print()
    print("Listening...")

    # Register the hotkey
    # 'ctrl+alt' string tells keyboard library which keys to watch for
    # When both keys pressed together → capture_and_save() is called
    # Goal: Trigger capture anywhere, anytime with one key combo
    keyboard.add_hotkey(HOTKEY, capture_and_save)

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

# Run if executed directly
if __name__ == '__main__':
    start_listening()
