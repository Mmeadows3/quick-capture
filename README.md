# Quick Capture

Voice-to-text note capture using Windows' built-in dictation (Win+H). Completely free, no API keys needed.

## How to Use

1. **Double-click `start.bat`**
2. **Press Ctrl+Left Alt** - capture window opens
3. **Press Win+H** to start dictation (or just type)
4. **Speak your note** - Windows types it
5. **Press Enter** to save to `daily.org` (or Esc to cancel)

That's it!

## What It Does

```
Ctrl+Left Alt → Window opens → Win+H → Speak → Enter → 
Saves as "* [2026-07-17 13:45] Your note text"
```

## How It Works (Modular Design)

Built from small, testable modules that each do one thing:

### 1. `save_note.py` - Core saving functionality
- Takes text and saves to daily.org
- Adds timestamp in org-mode format
- **Test it:** `python save_note.py`

### 2. `capture_window.py` - GUI window
- Shows a text box for typing/dictation
- Returns entered text or empty if cancelled
- **Test it:** `python capture_window.py`

### 3. `quick_capture.py` - Combines window + save
- Uses capture_window.py to get text
- Uses save_note.py to save it
- **Test it:** `python quick_capture.py`

### 4. `hotkey_listener.py` - Listens for Ctrl+Left Alt
- Waits for hotkey press
- Calls quick_capture.py when pressed
- **Run it:** `python hotkey_listener.py`

### 5. `start.bat` - Easy launcher
- Checks Python is installed
- Installs keyboard library if needed
- Runs hotkey_listener.py

## Files

```
quick-capture/
├── start.bat              # Double-click to start
├── hotkey_listener.py     # Listens for Ctrl+Left Alt
├── quick_capture.py       # Combines window + save
├── capture_window.py      # Shows text box window
├── save_note.py          # Saves to daily.org
└── requirements.txt      # Just 'keyboard' library
```

## First Time Setup

Windows dictation should already work. If Win+H doesn't work:

1. **Settings** (Win+I)
2. **Privacy & Security** → **Speech**
3. Turn on **Online speech recognition**
4. **Time & Language** → **Typing** → **Voice typing** = ON

## Why This Design?

**Incremental:** Each module is a small step
- save_note.py = just file writing
- capture_window.py = just the GUI
- Each piece works independently

**Cumulative:** Later pieces build on earlier ones
- quick_capture.py uses capture_window.py + save_note.py
- hotkey_listener.py uses quick_capture.py

**Didactic:** Easy to understand and modify
- Each file has comments explaining what and why
- Can test each piece separately
- Can change one piece without breaking others

## Customization

**Different hotkey?** Edit `HOTKEY` in `hotkey_listener.py`:
```python
HOTKEY = 'f9'  # or 'ctrl+shift+n', etc.
```

**Different save location?** Edit `DAILY_ORG_PATH` in `save_note.py`:
```python
DAILY_ORG_PATH = r'C:\path\to\your\notes.org'
```

**Different timestamp format?** Edit the `strftime()` in `save_note.py`:
```python
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
```

## Cost

**$0** - Uses Windows' free cloud dictation (same as pressing Win+H manually)

## Troubleshooting

**"Python not found"**
- Install from https://python.org/downloads/
- Make sure to check "Add Python to PATH"

**Hotkey doesn't work**
- May need to run `start.bat` as administrator
- Check if another app is using Ctrl+Left Alt

**Win+H doesn't open dictation**
- Check Settings → Privacy → Speech is ON
- Check Settings → Typing → Voice typing is ON
- Try pressing Win+H outside the app first to test

## License

MIT
