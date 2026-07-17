"""
Configuration for Quick Capture.

Centralizes all customizable settings so users can modify behavior
without touching the core modules.
"""

class Config:
    """Application settings - where to save, what hotkey to use, timestamp format."""

    def __init__(self):
        # File path for captured notes (org-mode format)
        self.daily_org_path = r'C:\Users\Micah\shared\daily.org'

        # System-wide hotkey combination
        self.hotkey = 'ctrl+alt'

        # Timestamp format for each note entry
        self.timestamp_format = "%Y-%m-%d %H:%M"

        # Template for each org-mode entry
        self.entry_format = "* [{timestamp}] {text}\n"
