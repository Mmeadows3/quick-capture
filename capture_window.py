"""
capture_window.py - GUI window for capturing text

This module does ONE thing: shows a window with a text box and returns the text.
"""
import tkinter as tk

def show_capture_window():
    """
    Show a capture window and return the text entered.

    Returns:
        str: The text entered (empty string if cancelled)

    How it works:
        1. Opens a window with a text box
        2. Text box is focused and ready for typing
        3. User types or dictates (Win+H)
        4. Press Enter to accept, Esc to cancel
        5. Returns the text
    """
    # This will store the result
    result = {"text": ""}

    # Create the window
    root = tk.Tk()
    root.title("Quick Capture")
    root.geometry("600x300")
    root.configure(bg='#1e1e1e')  # Dark background

    # Stay on top of other windows
    root.attributes('-topmost', True)

    # Center on screen
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # Instructions label
    label = tk.Label(
        root,
        text="Type or press Win+H to dictate\nEnter = Save | Esc = Cancel",
        font=('Segoe UI', 10),
        bg='#1e1e1e',
        fg='#ffffff'
    )
    label.pack(pady=10)

    # Text entry box
    text_box = tk.Text(
        root,
        font=('Segoe UI', 12),
        wrap=tk.WORD,  # Wrap at word boundaries
        bg='#2d2d2d',  # Slightly lighter dark
        fg='#ffffff',  # White text
        insertbackground='#ffffff',  # White cursor
        relief=tk.FLAT,
        padx=10,
        pady=10
    )
    text_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    # Focus the text box so it's ready for typing
    text_box.focus_set()

    def on_save():
        """Called when user presses Enter"""
        result["text"] = text_box.get('1.0', 'end-1c').strip()  # Get all text, strip whitespace
        root.destroy()

    def on_cancel():
        """Called when user presses Esc"""
        result["text"] = ""
        root.destroy()

    # Bind keyboard shortcuts
    root.bind('<Return>', lambda e: on_save())  # Enter key
    root.bind('<Escape>', lambda e: on_cancel())  # Escape key

    # Make window modal-like (grabs focus)
    root.focus_force()
    root.lift()

    # Show window and wait for it to close
    root.mainloop()

    # Return the text that was entered
    return result["text"]

# Test if run directly
if __name__ == '__main__':
    print("Opening capture window...")
    print("(Type something and press Enter, or press Esc to cancel)")

    text = show_capture_window()

    if text:
        print(f"\n[OK] You entered: {text}")
    else:
        print("\n[CANCELLED] No text entered")
