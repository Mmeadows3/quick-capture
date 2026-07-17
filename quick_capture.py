"""
quick_capture.py - Combines window and save functionality

This module does ONE thing: shows capture window, then saves the text.
"""
from capture_window import show_capture_window
from save_note import save_note

def capture_and_save():
    """
    Show capture window and save the result.

    How it works:
        1. Opens capture window (from capture_window.py)
        2. User enters text
        3. If they press Enter, saves to daily.org (using save_note.py)
        4. If they press Esc, does nothing

    Returns:
        bool: True if saved, False if cancelled
    """
    print("Opening capture window...")

    # Show the window and get the text
    text = show_capture_window()

    # If user cancelled (Esc) or entered nothing, don't save
    if not text:
        print("[CANCELLED] No text to save")
        return False

    # Save the text
    success = save_note(text)

    if success:
        # f"..." = formatted string (inserts {text} variable into the string)
        # Goal: Show what was saved so user knows it worked
        print(f"[OK] Saved: {text}")
        return True
    else:
        print("[FAIL] Could not save")
        return False

# Test if run directly
if __name__ == '__main__':
    # '=' * 60 creates a line of 60 equal signs (visual separator)
    # Goal: Makes output easy to read with clear sections
    print("=" * 60)
    print("Quick Capture Test")
    print("=" * 60)
    print()

    # Run one capture
    capture_and_save()

    print()
    print("=" * 60)
