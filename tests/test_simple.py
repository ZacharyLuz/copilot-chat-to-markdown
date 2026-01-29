#!/usr/bin/env python3
"""
Simple test runner that doesn't require pytest.
Can be run directly: python3 tests/test_simple.py
"""

import sys
import os
import json
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_to_markdown import (
    validate_file_size,
    sanitize_file_path,
    validate_output_path,
    format_message_text,
    extract_text_from_response_part,
    MAX_FILE_SIZE_BYTES
)


class TestRunner:
    """Simple test runner"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, message=""):
        """Assert that two values are equal"""
        if actual == expected:
            self.passed += 1
            return True
        else:
            self.failed += 1
            error = f"FAIL: {message}\n  Expected: {expected}\n  Got: {actual}"
            self.errors.append(error)
            print(f"✗ {error}")
            return False
    
    def assert_in(self, needle, haystack, message=""):
        """Assert that needle is in haystack"""
        if needle in haystack:
            self.passed += 1
            return True
        else:
            self.failed += 1
            error = f"FAIL: {message}\n  Expected '{needle}' in '{haystack}'"
            self.errors.append(error)
            print(f"✗ {error}")
            return False
    
    def assert_raises(self, exception_type, func, *args, **kwargs):
        """Assert that function raises specific exception"""
        try:
            func(*args, **kwargs)
            self.failed += 1
            error = f"FAIL: Expected {exception_type.__name__} to be raised"
            self.errors.append(error)
            print(f"✗ {error}")
            return False
        except exception_type:
            self.passed += 1
            return True
        except Exception as e:
            self.failed += 1
            error = f"FAIL: Expected {exception_type.__name__} but got {type(e).__name__}: {e}"
            self.errors.append(error)
            print(f"✗ {error}")
            return False
    
    def report(self):
        """Print test report"""
        total = self.passed + self.failed
        print("\n" + "="*60)
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\n{self.failed} tests failed:")
            for error in self.errors:
                print(f"  {error}")
            return 1
        else:
            print("✓ All tests passed!")
            return 0


def run_tests():
    """Run all tests"""
    runner = TestRunner()
    
    print("Running tests...\n")
    
    # Test path sanitization
    print("Testing path sanitization...")
    runner.assert_equal(
        sanitize_file_path('file.txt'),
        'file.txt',
        "Basic filename"
    )
    runner.assert_equal(
        sanitize_file_path('/path/to/file.txt'),
        'file.txt',
        "Absolute path"
    )
    runner.assert_equal(
        sanitize_file_path('../../etc/passwd'),
        'passwd',
        "Path traversal attack"
    )
    runner.assert_equal(
        sanitize_file_path('../../../etc/shadow'),
        'shadow',
        "Multiple path traversal"
    )
    print("✓ Path sanitization tests completed\n")
    
    # Test text formatting
    print("Testing text formatting...")
    result = format_message_text("Hello world")
    runner.assert_in("Hello world", result, "Basic text formatting")
    
    empty_result = format_message_text("")
    runner.assert_equal(empty_result, "", "Empty text handling")
    
    unicode_text = "Hello 世界 🌍"
    unicode_result = format_message_text(unicode_text)
    runner.assert_in("世界", unicode_result, "Unicode handling")
    print("✓ Text formatting tests completed\n")
    
    # Test response part extraction
    print("Testing response part extraction...")
    part = {"value": "Test content"}
    result = extract_text_from_response_part(part)
    runner.assert_equal(result, "Test content", "Extract from dict with value")
    
    metadata_part = {"kind": "inlineReference", "value": "Should be skipped"}
    result = extract_text_from_response_part(metadata_part)
    runner.assert_equal(result, "", "Skip metadata")
    print("✓ Response part extraction tests completed\n")
    
    # Test file size validation
    print("Testing file size validation...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{"test": "data"}')
        temp_file = f.name
    
    try:
        validate_file_size(temp_file)
        runner.passed += 1
        print("✓ File size validation accepts valid files")
    except Exception as e:
        runner.failed += 1
        runner.errors.append(f"File size validation failed: {e}")
        print(f"✗ File size validation failed: {e}")
    finally:
        os.unlink(temp_file)
    print("✓ File size validation tests completed\n")
    
    # Test output path validation
    print("Testing output path validation...")
    with tempfile.TemporaryDirectory() as tmpdir:
        safe_path = os.path.join(tmpdir, "output.md")
        try:
            validate_output_path(safe_path)
            runner.passed += 1
            print("✓ Output path validation accepts safe paths")
        except Exception as e:
            runner.failed += 1
            runner.errors.append(f"Output path validation failed: {e}")
            print(f"✗ Output path validation failed: {e}")
    
    # Test system directory blocking (Unix only)
    if os.name != 'nt':
        runner.assert_raises(
            ValueError,
            validate_output_path,
            '/etc/test.md'
        )
        print("✓ Output path validation blocks system directories")
    
    print("✓ Output path validation tests completed\n")
    
    # Test constants
    print("Testing security constants...")
    runner.assert_equal(
        MAX_FILE_SIZE_BYTES,
        100 * 1024 * 1024,
        "MAX_FILE_SIZE_BYTES is 100MB"
    )
    print("✓ Security constants tests completed\n")
    
    # Integration test
    print("Testing integration with sample file...")
    sample_file = "samples/chat.json"
    if os.path.exists(sample_file):
        try:
            validate_file_size(sample_file)
            with open(sample_file, 'r') as f:
                data = json.load(f)
            runner.passed += 1
            print("✓ Sample file is valid and can be processed")
        except Exception as e:
            runner.failed += 1
            runner.errors.append(f"Sample file test failed: {e}")
            print(f"✗ Sample file test failed: {e}")
    else:
        print("⚠ Sample file not found, skipping integration test")
    
    # Print report
    return runner.report()


if __name__ == '__main__':
    sys.exit(run_tests())
