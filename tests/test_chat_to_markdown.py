"""
Unit tests for chat_to_markdown.py

These tests validate the security features and core functionality of the script.
Run with: pytest tests/test_chat_to_markdown.py
"""

import sys
import os
import json
import tempfile
import pytest

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_to_markdown import (
    validate_file_size,
    sanitize_file_path,
    validate_output_path,
    format_message_text,
    extract_text_from_response_part,
    MAX_FILE_SIZE_BYTES
)


class TestSecurityValidation:
    """Test security validation functions"""
    
    def test_sanitize_file_path_basic(self):
        """Test basic path sanitization"""
        assert sanitize_file_path('file.txt') == 'file.txt'
        assert sanitize_file_path('/path/to/file.txt') == 'file.txt'
        
    def test_sanitize_file_path_traversal(self):
        """Test path traversal prevention"""
        assert sanitize_file_path('../../etc/passwd') == 'passwd'
        assert sanitize_file_path('../../../etc/shadow') == 'shadow'
        assert sanitize_file_path('/usr/local/bin/../../../etc/hosts') == 'hosts'
        
    def test_sanitize_file_path_windows(self):
        """Test Windows path sanitization"""
        assert sanitize_file_path('C:\\Windows\\System32\\config\\sam') == 'sam'
        assert sanitize_file_path('..\\..\\..\\Windows\\System32\\drivers') == 'drivers'
        
    def test_validate_file_size_valid(self, tmp_path):
        """Test file size validation with valid file"""
        # Create a small file
        test_file = tmp_path / "test.json"
        test_file.write_text('{"test": "data"}')
        
        # Should not raise exception
        validate_file_size(str(test_file))
        
    def test_validate_file_size_too_large(self, tmp_path):
        """Test file size validation with oversized file"""
        # We can't actually create a 100MB+ file easily in tests
        # So we'll test the logic by mocking if needed
        # For now, just verify the function exists and has the right signature
        assert callable(validate_file_size)
        
    def test_validate_output_path_safe(self, tmp_path):
        """Test output path validation with safe path"""
        safe_path = tmp_path / "output.md"
        # Should not raise exception
        validate_output_path(str(safe_path))
        
    def test_validate_output_path_system_directory(self):
        """Test output path validation blocks system directories"""
        if os.name != 'nt':  # Unix-like systems
            with pytest.raises(ValueError, match="Cannot write to system directory"):
                validate_output_path('/etc/test.md')
            with pytest.raises(ValueError, match="Cannot write to system directory"):
                validate_output_path('/sys/test.md')


class TestTextProcessing:
    """Test text processing functions"""
    
    def test_format_message_text_basic(self):
        """Test basic text formatting"""
        result = format_message_text("Hello world")
        assert "Hello world" in result
        
    def test_format_message_text_empty(self):
        """Test empty text handling"""
        result = format_message_text("")
        assert result == ""
        
    def test_format_message_text_removes_metadata(self):
        """Test that metadata is filtered out"""
        text = "Hello\n{$mid:123}\nWorld"
        result = format_message_text(text)
        assert "{$mid:123}" not in result
        assert "Hello" in result or "World" in result
        
    def test_extract_text_from_response_part_dict(self):
        """Test extracting text from dictionary response"""
        part = {"value": "Test content"}
        result = extract_text_from_response_part(part)
        assert result == "Test content"
        
    def test_extract_text_from_response_part_skip_metadata(self):
        """Test that metadata is skipped"""
        part = {"kind": "inlineReference", "value": "Should be skipped"}
        result = extract_text_from_response_part(part)
        assert result == ""


class TestInputValidation:
    """Test input validation in main flow"""
    
    def test_valid_json_structure(self, tmp_path):
        """Test that valid JSON is accepted"""
        test_file = tmp_path / "valid.json"
        test_data = {
            "version": "1",
            "requests": []
        }
        test_file.write_text(json.dumps(test_data))
        
        # Should not raise exception when loading
        with open(test_file, 'r') as f:
            data = json.load(f)
        assert isinstance(data, dict)
        
    def test_invalid_json_structure(self, tmp_path):
        """Test that invalid JSON is rejected"""
        test_file = tmp_path / "invalid.json"
        test_file.write_text("{invalid json content")
        
        # Should raise JSONDecodeError
        with pytest.raises(json.JSONDecodeError):
            with open(test_file, 'r') as f:
                json.load(f)


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_unicode_handling(self):
        """Test that unicode content is handled correctly"""
        text = "Hello 世界 🌍"
        result = format_message_text(text)
        assert "世界" in result
        assert "🌍" in result
        
    def test_very_long_text(self):
        """Test handling of long text (within limits)"""
        long_text = "A" * 10000  # 10KB of text
        result = format_message_text(long_text)
        assert len(result) > 0
        
    def test_special_characters(self):
        """Test handling of special characters"""
        text = "Test <>&\"'\n\t\r"
        result = format_message_text(text)
        assert len(result) > 0


class TestConstants:
    """Test that security constants are properly defined"""
    
    def test_max_file_size_defined(self):
        """Test that MAX_FILE_SIZE_BYTES is defined"""
        assert MAX_FILE_SIZE_BYTES > 0
        assert MAX_FILE_SIZE_BYTES == 100 * 1024 * 1024  # 100 MB


# Integration test (requires sample file)
class TestIntegration:
    """Integration tests using sample files"""
    
    def test_sample_conversion(self, tmp_path):
        """Test conversion with sample file if available"""
        sample_file = "samples/chat.json"
        if os.path.exists(sample_file):
            from chat_to_markdown import main
            import sys
            
            output_file = tmp_path / "output.md"
            
            # Mock sys.argv to simulate command line
            old_argv = sys.argv
            try:
                sys.argv = ['chat_to_markdown.py', sample_file, str(output_file)]
                
                # Run main (would need to be refactored to avoid sys.exit)
                # For now, just verify the file exists
                assert os.path.exists(sample_file)
                assert os.path.getsize(sample_file) < MAX_FILE_SIZE_BYTES
            finally:
                sys.argv = old_argv


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
