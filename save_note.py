"""
save_note.py - Core functionality for saving notes to daily.org

This module does ONE thing: takes text and appends it to daily.org with a timestamp.
"""
from datetime import datetime
from pathlib import Path

# Where to save notes
DAILY_ORG_PATH = r'C:\Users\Micah\shared\daily.org'

def save_note(text):
    """
    Save a note to daily.org with timestamp

    Args:
        text: The note content to save

    Example:
        save_note("This is my note")
        # Writes: "* [2026-07-17 14:45] This is my note"
    """
    # Don't save empty notes
    if not text.strip():
        return False

    # Create timestamp in format: [2026-07-17 14:45]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Format as org-mode bullet: * [timestamp] text
    entry = f"* [{timestamp}] {text.strip()}\n"

    # Make sure the directory exists
    # (Path().parent gets the folder, mkdir creates it if needed)
    Path(DAILY_ORG_PATH).parent.mkdir(parents=True, exist_ok=True)

    # Append to file (mode 'a' = append, encoding for special characters)
    with open(DAILY_ORG_PATH, 'a', encoding='utf-8') as f:
        f.write(entry)

    return True

# Test if run directly
if __name__ == '__main__':
    print("Testing save_note...")

    # Try saving a test note
    test_text = "Test note from save_note.py"
    success = save_note(test_text)

    if success:
        print("[OK] Saved test note")
        print(f"     Check: {DAILY_ORG_PATH}")
    else:
        print("[FAIL] Failed to save")
