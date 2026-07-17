# Voice Input Project

Voice-to-text dictation that integrates Windows 11's built-in speech recognition (Win+H) with automatic text capture to your daily notes.

## Features

- Uses Windows 11's high-accuracy dictation (Win+H)
- Minimal window with aggressive focus control (prevents text duplication)
- Auto-detects when you stop speaking (5s stable detection)
- Manual finish with Ctrl + Left Alt
- Lock mechanism prevents multiple instances
- Appends as bullet points to daily.org
- Visual notifications for feedback

## Requirements

- Windows 11 (for Win+H dictation)
- Python 3.7+
- AutoHotkey v2.0
- Python packages: tkinter, keyboard, winotify

## Installation

1. Install Python dependencies:
```bash
pip install keyboard winotify
```

2. Enable Windows speech recognition:
   - Open Settings (Win+I)
   - Go to Privacy & Security > Speech
   - Turn on "Online speech recognition"

3. Enable microphone access:
   - Settings > Privacy & Security > Microphone
   - Ensure "Microphone access" and "Let apps access your microphone" are ON

## Usage

### Quick Start (Recommended)

```bash
python start.py
```

This will:
1. Run tests to verify everything works
2. Start the AutoHotkey listener
3. Enable **Ctrl + Left Alt** hotkey for voice input

### Manual Steps

1. Run `voice_to_file.ahk` (or start via start.py)
2. Press **Ctrl + Left Alt** to start dictation
3. Speak into your microphone
4. Press **Ctrl + Left Alt** again to finish (or wait 5s after stopping)
5. Text is appended to `daily.org` as a bullet point

## Testing

Run the simplified test suite:

```bash
python tests/test_simplified.py
```

Tests verify:
1. Voice-to-text capture works
2. File writing works (uses dummy file, no pollution)

## Configuration

Edit `voice_to_file.py` to change:

- `OUTPUT_FILE` - Where to save captured text (default: `C:\Users\Micah\shared\daily.org`)
- `check_count >= 10` - Auto-complete delay (10 checks × 500ms = 5 seconds)
- `max_checks = 60` - Maximum timeout (60 checks × 500ms = 30 seconds)

## How It Works

1. **Hotkey pressed**: Ctrl + Left Alt triggers the Python script
2. **Focus control**: Window aggressively claims focus using `focus_force()`, `lift()`, and `update()`
3. **Speech trigger**: Sends Win+H to activate Windows dictation
4. **Text monitoring**: Checks text box every 500ms for changes
5. **Auto-complete**: After 5 seconds of no changes, automatically finishes
6. **Manual finish**: Ctrl + Left Alt also stops dictation immediately
7. **Save**: Appends text as bullet point to daily.org

## Troubleshooting

**Text appearing in multiple locations**
- The script now uses `focus_force()` and aggressive window activation
- If still happening, increase the delay in `root.after(1000, trigger_dictation)` to 1500ms or 2000ms

**"To use voice typing, select a text box"**
- Window focus issue - restart the script
- Check if another instance is running (delete `.voice_lock` if stuck)

**Getting cut off early**
- Increase `check_count >= 10` to a higher value (e.g., 20 for 10 seconds)
- Use Ctrl + Left Alt to manually finish when ready

**Multiple instances / lag**
- Delete `.voice_lock` file if stuck
- Lock mechanism normally prevents this automatically

**No speech detected**
- Check microphone permissions
- Test microphone with Win+H outside this app
- Ensure "Online speech recognition" is enabled in Windows Settings

## Project Structure

```
voice_input/
├── voice_to_file.py          # Main voice capture script
├── voice_to_file.ahk         # AutoHotkey hotkey listener (Ctrl + Left Alt)
├── start.py                  # Launcher with tests
└── tests/
    └── test_simplified.py    # Streamlined test suite (2 tests)
```

## License

MIT
