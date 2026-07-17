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
    # When F9 is pressed, capture_and_save() will be called
    keyboard.add_hotkey(HOTKEY, capture_and_save)

    # Keep the program running
    # This blocks until Ctrl+C is pressed
    try:
        keyboard.wait()  # Wait forever (until interrupted)
    except KeyboardInterrupt:
        print("\n\n[EXIT] Shutting down...")

# Run if executed directly
if __name__ == '__main__':
    start_listening()
