import sys
import tkinter as tk
import keyboard
from pathlib import Path
from winotify import Notification
import ctypes
import time

# Windows API functions for forcing window focus
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def force_window_to_foreground(hwnd):
    """Force a window to the foreground using Windows API"""
    # Get the current foreground window
    foreground = user32.GetForegroundWindow()

    # Get current thread and foreground thread IDs
    current_thread = kernel32.GetCurrentThreadId()
    foreground_thread = user32.GetWindowThreadProcessId(foreground, None)

    # Attach to the foreground thread to allow SetForegroundWindow to work
    if foreground_thread != current_thread:
        user32.AttachThreadInput(foreground_thread, current_thread, True)
        user32.BringWindowToTop(hwnd)
        user32.ShowWindow(hwnd, 5)  # SW_SHOW
        user32.SetForegroundWindow(hwnd)
        user32.AttachThreadInput(foreground_thread, current_thread, False)
    else:
        user32.BringWindowToTop(hwnd)
        user32.ShowWindow(hwnd, 5)  # SW_SHOW
        user32.SetForegroundWindow(hwnd)

    # Ensure window is focused
    user32.SetFocus(hwnd)
    return True

OUTPUT_FILE = Path(r"C:\Users\Micah\shared\daily.org")
LOCK_FILE = Path(r"C:\Users\Micah\shared\.voice_lock")

def acquire_lock():
    if LOCK_FILE.exists():
        return False
    LOCK_FILE.write_text("locked")
    return True

def release_lock():
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()

last_text = ""
check_count = 0
max_checks = 60  # 30 seconds max (60 checks at 500ms)
total_checks = 0

def trigger_dictation():
    # Get window handle
    hwnd = root.winfo_id()

    # Force window to foreground using Windows API
    root.lift()
    root.focus_force()
    text_box.focus_force()
    root.update()

    # Use Windows API to force activation
    force_window_to_foreground(hwnd)

    # Additional delay to ensure window is fully activated
    time.sleep(0.3)
    root.update()

    Notification(app_id="Voice Input", title="Listening...", msg="Speak now (Ctrl+LAlt to finish)", duration="short").show()
    keyboard.press_and_release('win+h')
    # Start monitoring for when text stops changing
    root.after(500, check_for_completion)

def check_for_completion():
    global last_text, check_count, total_checks
    current_text = text_box.get("1.0", "end-1c")
    total_checks += 1

    # Manual finish with Ctrl + Left Alt
    if keyboard.is_pressed('ctrl+alt'):
        finish_dictation()
        return

    # Max timeout reached
    if total_checks >= max_checks:
        finish_dictation()
        return

    # If text hasn't changed, increment counter
    if current_text == last_text:
        check_count += 1
        # If stable for 5 seconds (10 checks at 500ms), we're done
        if check_count >= 10:
            finish_dictation()
            return
    else:
        # Text changed, reset counter
        check_count = 0
        last_text = current_text

    # Check again in 500ms
    root.after(500, check_for_completion)

def finish_dictation():
    text = text_box.get("1.0", "end-1c").strip()
    root.destroy()
    release_lock()  # Release lock when done

    if text:
        output = Path(sys.argv[1]) if len(sys.argv) > 1 else OUTPUT_FILE
        with open(output, "a", encoding="utf-8") as f:
            f.write(f"- {text}\n")
        Notification(app_id="Voice Input", title="Captured", msg=text, duration="short").show()
    else:
        Notification(app_id="Voice Input", title="No speech detected", msg="Try again", duration="short").show()

# Check if another instance is already running
if not acquire_lock():
    sys.exit(0)  # Silently exit if locked

# Create window - visible for testing
root = tk.Tk()
root.title("Voice Input")
root.geometry("300x100")
root.attributes('-topmost', True)  # Stay on top

text_box = tk.Text(root, height=3, width=30)
text_box.pack(padx=10, pady=10)

# Force window activation and focus
root.lift()
root.focus_force()
text_box.focus_force()
root.update()

# Get window handle and force to foreground
hwnd = root.winfo_id()
force_window_to_foreground(hwnd)

# Longer initial delay to ensure window is fully activated
root.after(1500, trigger_dictation)
root.mainloop()
