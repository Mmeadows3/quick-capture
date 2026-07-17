"""
config.py - Central configuration for Quick Capture

This module does ONE thing: holds all application state/configuration.
All other modules are stateless and receive config as input.

Why centralize config?
- Single source of truth for all settings
- Easy to test (pass different config to modules)
- Easy to change settings without modifying module code
"""
from pathlib import Path

class Config:
    """
    Configuration class - holds all application settings

    This is the ONLY place where application state lives.
    All other modules are pure functions that take config as input.
    """

    def __init__(self):
        # Where to save notes
        # Default: C:\Users\Micah\shared\daily.org
        self.daily_org_path = r'C:\Users\Micah\shared\daily.org'

        # Hotkey combination to trigger capture
        # Format: 'ctrl+alt' means both keys pressed together
        self.hotkey = 'ctrl+alt'

        # Timestamp format for notes
        # %Y-%m-%d %H:%M produces: 2026-07-17 14:30
        self.timestamp_format = "%Y-%m-%d %H:%M"

        # Org-mode entry format
        # {timestamp} and {text} will be replaced
        self.entry_format = "* [{timestamp}] {text}\n"

    @classmethod
    def default(cls):
        """
        Create default configuration

        Returns:
            Config: Default configuration instance
        """
        return cls()

# Create a default config instance for convenience
# Other modules can import this, or create their own Config()
default_config = Config.default()
