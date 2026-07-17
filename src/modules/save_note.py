"""
save_note.py - Stateless note saving functionality

This module does ONE thing: takes text and config, saves to file.
NO state - all inputs come from parameters.
"""
from datetime import datetime
from pathlib import Path
from config import default_config

def save_note(text, config=None):
    """
    Save a note to daily.org with timestamp

    This is a PURE FUNCTION:
    - Takes inputs (text, config)
    - Returns output (success boolean, message)
    - No global state, no side effects except file write

    Args:
        text: The note content to save
        config: Configuration object (uses default if None)

    Returns:
        tuple: (success: bool, message: str)
            - (True, filepath) if saved successfully
            - (False, error_message) if failed

    Example:
        from config import Config
        cfg = Config()
        cfg.daily_org_path = "C:/my/notes.org"
        success, msg = save_note("My note", cfg)
    """
    # Use default config if none provided
    if config is None:
        config = default_config

    # Don't save empty notes
    if not text.strip():
        return False, "Empty text - nothing to save"

    # Final safety check: reject PowerShell noise even if it got past earlier filters
    text_lower = text.lower()
    noise_keywords = ['windows powershell', 'copyright (c) microsoft', 'microsoft corporation']
    if any(keyword in text_lower for keyword in noise_keywords):
        return False, "Rejected: PowerShell noise detected"

    try:
        # Create timestamp using format from config
        # strftime = "string format time" - converts datetime to string
        # Format defined in config (e.g., "%Y-%m-%d %H:%M")
        timestamp = datetime.now().strftime(config.timestamp_format)

        # Format entry using template from config
        # f-string inserts {timestamp} and {text} into the template
        # Goal: Create entries like "* [2026-07-17 14:45] Your note here"
        entry = config.entry_format.format(timestamp=timestamp, text=text.strip())

        # Make sure the directory exists
        # Path().parent gets the folder, mkdir creates it if needed
        # exist_ok=True means don't error if it already exists
        Path(config.daily_org_path).parent.mkdir(parents=True, exist_ok=True)

        # Append to file
        # 'a' = append mode (adds to end without erasing existing content)
        # encoding='utf-8' = handles special characters like emoji, accents
        # Goal: Add our entry to the end of daily.org without losing old notes
        with open(config.daily_org_path, 'a', encoding='utf-8') as f:
            f.write(entry)

        return True, config.daily_org_path

    except PermissionError:
        return False, f"Permission denied writing to {config.daily_org_path}"
    except OSError as e:
        return False, f"File system error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

# Test if run directly
if __name__ == '__main__':
    print("Testing save_note...")

    # Create a test config with different path
    from config import Config
    test_config = Config()
    # Use the default path for testing

    # Try saving a test note
    test_text = "Test note from save_note.py"
    success, message = save_note(test_text, test_config)

    if success:
        print(f"[OK] Saved to: {message}")
    else:
        print(f"[FAIL] {message}")
