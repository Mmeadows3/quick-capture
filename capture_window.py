"""
capture_window.py - GUI window for capturing text (PowerShell version)

This module does ONE thing: shows a window with a text box and returns the text.
Uses PowerShell + Windows Forms for fast, native Windows GUI.
"""
import subprocess
from pathlib import Path

def show_capture_window():
    """
    Show a capture window and return the text entered.

    Returns:
        str: The text entered (empty string if cancelled)

    How it works:
        1. Calls PowerShell script (capture_window.ps1)
        2. PowerShell shows native Windows form
        3. User types or dictates (Win+H)
        4. Press Enter to accept, Esc to cancel
        5. PowerShell outputs the text, Python reads it

    Why PowerShell?
        - Faster startup than tkinter
        - Native Windows GUI (Windows Forms)
        - Better auto-focus on Windows
    """
    # Get the directory where this script is located
    # __file__ = path to this Python file
    # .parent = get the directory containing this file
    script_dir = Path(__file__).parent

    # Path to the PowerShell script
    # script_dir / "filename" = join path with filename
    ps_script = script_dir / "capture_window.ps1"

    # Run PowerShell script
    # subprocess.run() = run external program and wait for it to finish
    # 'powershell' = run PowerShell
    # '-ExecutionPolicy', 'Bypass' = allow script to run without security prompt
    # '-File', ps_script = run this script file
    # capture_output=True = capture what the script prints
    # text=True = return output as text (not bytes)
    # encoding='utf-8' = handle special characters correctly
    result = subprocess.run(
        ['powershell', '-ExecutionPolicy', 'Bypass', '-File', str(ps_script)],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    # Get the text from PowerShell output
    # result.stdout = what PowerShell printed to console
    # .strip() = remove leading/trailing whitespace
    # Goal: Return exactly what user typed, or empty string if cancelled
    return result.stdout.strip()

# Test if run directly
if __name__ == '__main__':
    print("Opening capture window...")
    print("(Type something and press Enter, or press Esc to cancel)")

    text = show_capture_window()

    if text:
        print(f"\n[OK] You entered: {text}")
    else:
        print("\n[CANCELLED] No text entered")
