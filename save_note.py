"""
save_note.py - Core functionality for saving notes to daily.org

This module does ONE thing: takes text and appends it to daily.org with a timestamp.
"""
from datetime import datetime
from pathlib import Path

# Where to save notes
# r'...' = raw string (backslashes are literal, not escape characters)
# This prevents '\U' from being interpreted as a unicode escape
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
    # strftime = "string format time" - converts datetime to string
    # %Y = 4-digit year (2026)
    # %m = 2-digit month (01-12)
    # %d = 2-digit day (01-31)
    # %H = 2-digit hour in 24-hour format (00-23)
    # %M = 2-digit minute (00-59)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Format as org-mode bullet: * [timestamp] text
    # f"..." = f-string (formatted string literal)
    # Inserts {timestamp} and {text.strip()} into the string
    # \n = newline character (moves to next line)
    # Goal: Create entries like "* [2026-07-17 14:45] Your note here"
    entry = f"* [{timestamp}] {text.strip()}\n"

    # Make sure the directory exists
    # (Path().parent gets the folder, mkdir creates it if needed)
    Path(DAILY_ORG_PATH).parent.mkdir(parents=True, exist_ok=True)

    # Append to file
    # 'a' = append mode (adds to end without erasing existing content)
    # 'w' would erase the file, 'r' would read-only, 'a' adds to the end
    # encoding='utf-8' = handles special characters like emoji, accents
    # Goal: Add our entry to the end of daily.org without losing old notes
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
