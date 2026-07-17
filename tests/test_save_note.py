"""
test_save_note.py - Tests for save_note module

Tests the stateless save_note function with different inputs.
"""
import sys
from pathlib import Path

# Add src to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import tempfile
import os
from config import Config
from modules.save_note import save_note

def test_save_note_basic():
    """Test that save_note writes to file correctly"""
    # Create a temporary file for testing
    # This way we don't pollute the real daily.org
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.org') as tmp:
        temp_path = tmp.name

    try:
        # Create config with temp path
        config = Config()
        config.daily_org_path = temp_path

        # Save a note
        test_text = "Test note"
        success, message = save_note(test_text, config)

        # Check it returned success
        assert success == True, "save_note should return True"
        assert temp_path in message, "Should return filepath on success"

        # Check file exists
        assert Path(temp_path).exists(), "File should exist"

        # Check content
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert test_text in content, "File should contain the note text"
        assert content.startswith("* ["), "Should start with org-mode bullet"
        assert "] " in content, "Should have timestamp format"

        print("[PASS] save_note basic test")
        return True

    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_save_note_empty():
    """Test that save_note rejects empty text"""
    config = Config()

    # Try to save empty text
    success, message = save_note("", config)

    assert success == False, "Should return False for empty text"
    assert "Empty" in message or "empty" in message, "Should explain why it failed"

    # Try whitespace only
    success, message = save_note("   ", config)

    assert success == False, "Should return False for whitespace"

    print("[PASS] save_note empty text test")
    return True

def test_save_note_creates_directory():
    """Test that save_note creates parent directory if needed"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create path with non-existent subdirectory
        test_path = Path(tmpdir) / "subdir" / "notes.org"

        config = Config()
        config.daily_org_path = str(test_path)

        # Save note (should create subdir)
        success, message = save_note("Test", config)

        assert success == True, "Should succeed"
        assert test_path.exists(), "Should create parent directory"

        print("[PASS] save_note directory creation test")
        return True

def test_save_note_rejects_powershell_noise():
    """Test that save_note rejects PowerShell banner text"""
    config = Config()

    # Test cases that should be rejected
    noise_cases = [
        "Windows PowerShell\nCopyright (C) Microsoft Corporation.",
        "Windows PowerShell\nCopyright (C) Microsoft Corporation. All rights reserved.\nSome other text",
        "microsoft corporation info",
    ]

    for text in noise_cases:
        success, message = save_note(text, config)
        assert success == False, f"Should reject PowerShell noise: {text[:30]}"
        assert "noise" in message.lower(), f"Should mention noise in error message"

    # Test cases that should be accepted
    valid_cases = [
        "I need to call Microsoft support tomorrow",
        "Review copyright license for the project",
        "Normal note about my day",
    ]

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.org') as tmp:
        temp_path = tmp.name

    try:
        config.daily_org_path = temp_path

        for text in valid_cases:
            success, message = save_note(text, config)
            assert success == True, f"Should accept valid text: {text[:30]}"

        print("[PASS] save_note PowerShell noise filtering test")
        return True

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def run_all_tests():
    """Run all save_note tests"""
    print("Testing save_note module...")
    print()

    tests = [
        test_save_note_basic,
        test_save_note_empty,
        test_save_note_creates_directory,
        test_save_note_rejects_powershell_noise
    ]

    for test in tests:
        if not test():
            print("[FAIL] Test suite failed")
            return False
        print()

    print("[SUCCESS] All save_note tests passed")
    return True

def test_save_note(quiet=False):
    """
    Wrapper for test_runner.py integration

    Runs all save_note tests with appropriate output level.
    """
    if quiet:
        # In quiet mode, just verify imports and basic functionality
        try:
            from modules.save_note import save_note
            from config import Config
            print("  [OK] Import save_note module")

            # Quick smoke test
            success, message = save_note("Test note", Config())
            if success:
                print("  [OK] save_note basic functionality")
                return True
            else:
                print(f"  [FAIL] save_note basic functionality: {message}")
                return False
        except Exception as e:
            print(f"  [FAIL] save_note tests: {e}")
            return False
    else:
        # Verbose mode - run full test suite
        print("\n[Testing save_note.py]")
        return run_all_tests()

if __name__ == '__main__':
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
