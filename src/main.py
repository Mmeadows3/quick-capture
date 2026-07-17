"""
main.py - Main entry point for Quick Capture

This is the MASTER module that:
1. Creates and manages application state (Config)
2. Wires together all the stateless modules
3. Starts the application

All other modules are stateless - this is the only place
where state is created and managed.
"""
from config import Config
from modules.hotkey_listener import start_listening
from modules.capture_window import show_capture_window
from modules.save_note import save_note

def capture_and_save(config):
    """
    Orchestration: Show capture window and save the result.

    This is the glue code that wires together:
    - capture_window (GUI behavior)
    - save_note (file I/O behavior)

    Args:
        config: Configuration object

    Returns:
        bool: True if saved, False if cancelled or failed
    """
    # Small delay to ensure hotkey is fully released before opening window
    # This prevents Ctrl+Alt from interfering with the GUI
    import time
    time.sleep(0.2)

    print("\n" + "=" * 60)
    print("Quick Capture - Opening window...")
    print("=" * 60)

    # Get text from GUI
    text = show_capture_window()

    # If cancelled or empty, don't save
    if not text:
        print("Cancelled\n")
        return False

    # Reject PowerShell noise that sometimes leaks through
    # These should never be legitimate user input
    noise_indicators = [
        'windows powershell',
        'copyright (c) microsoft',
        'microsoft corporation',
        'all rights reserved',
        'try the new cross-platform powershell',
        'https://aka.ms/pscore6',
        'loading personal and system profiles',
    ]
    text_lower = text.lower()

    # Check entire text
    for indicator in noise_indicators:
        if indicator in text_lower:
            print(f"⚠️  Rejected PowerShell noise (contains '{indicator}')")
            print(f"    Full text was: {repr(text[:100])}")
            print("=" * 60 + "\n")
            return False

    # Also reject if first line is ONLY PowerShell banner-like text
    # (not if it's part of a sentence)
    first_line = text.split('\n')[0].strip()
    banner_patterns = [
        'windows powershell',
        'copyright',
        'microsoft corporation',
    ]
    # Check if the ENTIRE first line matches a banner pattern (not just contains it)
    if first_line.lower() in banner_patterns or \
       (len(first_line) < 30 and any(pattern in first_line.lower() for pattern in ['powershell', 'copyright (c)'])):
        print(f"⚠️  Rejected PowerShell noise (banner first line: '{first_line}')")
        print("=" * 60 + "\n")
        return False

    # Save to file
    success, message = save_note(text, config)

    if success:
        print(f"Saved: {text}")
        print("=" * 60 + "\n")
        return True
    else:
        print(f"Error: {message}")
        print("=" * 60 + "\n")
        return False

def main():
    """
    Main entry point - creates config and starts listener

    This is where APPLICATION STATE is managed:
    - Creates Config instance
    - Passes it to all stateless modules
    - Wires everything together
    """
    # Create application configuration
    # This is the ONLY place where app state lives
    config = Config()

    # You could customize config here:
    # config.daily_org_path = "D:/notes/daily.org"
    # config.hotkey = 'f9'

    # Create the callback that will be triggered by hotkey
    # It receives the config and passes it through
    def on_capture():
        return capture_and_save(config)

    # Start listening with our config and callback
    # All state flows through parameters - no globals
    start_listening(
        hotkey=config.hotkey,
        on_trigger=on_capture,
        config=config,
        quiet=True  # start.bat handles the banner
    )

if __name__ == '__main__':
    main()
