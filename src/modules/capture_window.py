"""
GUI window for text capture.

Uses PowerShell + Windows Forms for fast startup and reliable auto-focus.
Better than tkinter on Windows for this use case.
"""
import subprocess
from pathlib import Path

def show_capture_window():
    """
    Show capture window, return entered text.

    Flow:
    1. Launch PowerShell GUI (capture_window.ps1)
    2. User types or dictates (Win+H)
    3. Enter = save, Esc = cancel
    4. Return captured text

    Returns:
        str: Captured text (empty if cancelled)
    """
    # Find PowerShell GUI script relative to this file
    # __file__ is src/modules/capture_window.py, walk up to project root
    project_root = Path(__file__).parent.parent.parent
    ps_script = project_root / "gui" / "capture_window.ps1"

    # Launch PowerShell without showing console window
    # -WindowStyle Hidden: only show the GUI form, not PowerShell console
    # -NoProfile/-NoLogo: prevent startup scripts/banners from adding noise
    # -ExecutionPolicy Bypass: allow script to run regardless of user policy
    result = subprocess.run(
        ['powershell', '-WindowStyle', 'Hidden', '-NoProfile', '-NoLogo',
         '-ExecutionPolicy', 'Bypass', '-File', str(ps_script)],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    return result.stdout.strip()

# Quick test when run directly
if __name__ == '__main__':
    print("Opening capture window...")
    print("(Type something and press Enter, or press Esc to cancel)")
    text = show_capture_window()
    print(f"[{'OK' if text else 'CANCELLED'}] {repr(text)}")
