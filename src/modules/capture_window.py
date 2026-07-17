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
    # Get the project root directory
    # __file__ = path to this Python file (in src/modules/)
    # .parent = modules/ directory
    # .parent again = src/ directory
    # .parent once more = project root
    project_root = Path(__file__).parent.parent.parent

    # Path to the PowerShell script in gui/
    ps_script = project_root / "gui" / "capture_window.ps1"

    print(f"[DEBUG] Launching PowerShell window: {ps_script}")

    # Run PowerShell script
    # -WindowStyle Hidden hides the PowerShell console (we only want the Forms GUI)
    # -NoProfile prevents profile scripts from running and outputting text
    # -NoLogo suppresses copyright banner
    result = subprocess.run(
        ['powershell', '-WindowStyle', 'Hidden', '-NoProfile', '-NoLogo', '-ExecutionPolicy', 'Bypass', '-File', str(ps_script)],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    # Return exactly what the user typed (or empty if cancelled)
    captured_text = result.stdout.strip()

    # DEBUG: Show what we captured
    print(f"[TEMP DEBUG] Captured: {repr(captured_text)}")
    print(f"[TEMP DEBUG] Return code: {result.returncode}")
    if result.stderr:
        print(f"[TEMP DEBUG] PowerShell stderr:")
        for line in result.stderr.strip().split('\n'):
            print(f"  {line}")

    return captured_text

# Test if run directly
if __name__ == '__main__':
    print("Opening capture window...")
    print("(Type something and press Enter, or press Esc to cancel)")

    text = show_capture_window()

    if text:
        print(f"\n[OK] You entered: {text}")
    else:
        print("\n[CANCELLED] No text entered")
