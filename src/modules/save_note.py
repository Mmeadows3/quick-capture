"""
Persistent storage for captured notes.

Appends timestamped entries to daily.org in org-mode format.
"""
from datetime import datetime
from pathlib import Path

def save_note(text, config):
    """
    Append timestamped note to daily.org file.

    Args:
        text: Note content to save
        config: Config object with file path and format settings

    Returns:
        (success: bool, message: str) - Success flag and filepath or error message
    """
    if not text.strip():
        return False, "Empty text - nothing to save"

    # Safety check: reject PowerShell startup banners that sometimes leak through
    text_lower = text.lower()
    noise_keywords = ['windows powershell', 'copyright (c) microsoft', 'microsoft corporation']
    if any(keyword in text_lower for keyword in noise_keywords):
        return False, "Rejected: PowerShell noise detected"

    try:
        # Format the entry: "* [2026-07-17 14:30] Your note text"
        timestamp = datetime.now().strftime(config.timestamp_format)
        entry = config.entry_format.format(timestamp=timestamp, text=text.strip())

        # Create directory if it doesn't exist (first-time setup)
        Path(config.daily_org_path).parent.mkdir(parents=True, exist_ok=True)

        # Append to file (preserves existing notes)
        with open(config.daily_org_path, 'a', encoding='utf-8') as f:
            f.write(entry)

        return True, config.daily_org_path

    except PermissionError:
        return False, f"Permission denied writing to {config.daily_org_path}"
    except OSError as e:
        return False, f"File system error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

# Quick test when run directly
if __name__ == '__main__':
    from config import Config
    test_config = Config()
    success, message = save_note("Test note from save_note.py", test_config)
    print(f"[{'OK' if success else 'FAIL'}] {message}")
