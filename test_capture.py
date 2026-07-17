"""Quick test of capture window"""
import sys
sys.path.insert(0, 'src')

from modules.capture_window import show_capture_window

print("Opening window...")
result = show_capture_window()
print(f"Result: {repr(result)}")
print(f"Length: {len(result)}")
