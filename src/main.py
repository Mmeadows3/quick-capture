"""
Quick Capture - Application entry point.

Wires together all modules (config, GUI, storage, hotkey listener) to enable
quick note capture from anywhere on the system.
"""
import time
from config import Config
from modules.hotkey_listener import start_listening
from modules.capture_window import show_capture_window
from modules.save_note import save_note

def capture_and_save(config):
    """
    Complete capture workflow: show GUI → save to file.

    Args:
        config: Config object with file path and format settings

    Returns:
        bool: True if saved, False if cancelled or failed
    """
    # Small delay ensures hotkey fully released before GUI opens
    # (prevents Ctrl+Alt from interfering with text input)
    time.sleep(0.2)

    print("\n" + "=" * 60)
    print("Quick Capture - Opening window...")
    print("=" * 60)

    # Get text from user (typing or Win+H dictation)
    text = show_capture_window()

    if not text:
        print("Cancelled\n")
        return False

    # Save to file with timestamp
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
    Entry point - create config, wire components, start listening.
    """
    # Load configuration (customizable: file path, hotkey, formats)
    config = Config()

    # Optional customization point:
    # config.daily_org_path = "D:/notes/daily.org"
    # config.hotkey = 'f9'

    # Create callback that uses our config
    def on_capture():
        return capture_and_save(config)

    # Start system-wide hotkey listener (runs until Ctrl+C)
    # quiet=True because start.bat already printed banner
    start_listening(
        hotkey=config.hotkey,
        on_trigger=on_capture,
        config=config,
        quiet=True
    )

if __name__ == '__main__':
    main()
