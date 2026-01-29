# Security Policy

## Overview

This project takes security seriously. This document outlines the security measures implemented in the codebase and how to report security vulnerabilities.

## Security Features

### Input Validation

#### File Size Limits
- **Maximum input file size**: 100 MB
- **Purpose**: Prevents denial-of-service (DoS) attacks through memory exhaustion
- **Implementation**: Files are checked before loading into memory

```python
# Validation occurs automatically when running the script
python chat_to_markdown.py input.json output.md
```

If a file exceeds the limit, you'll see:
```
Error: Input file is too large: 150.5 MB (maximum: 100 MB). This limit prevents denial-of-service attacks.
```

#### Path Traversal Protection
- **File paths are sanitized**: All file paths extracted from the JSON are sanitized to prevent path traversal attacks
- **Only basenames are used**: For display purposes, only the filename is shown, not the full path
- **No directory access**: Prevents malicious JSON from accessing files outside the intended scope

Example of protected pattern:
```json
{
  "file": "../../etc/passwd"  // Sanitized to just "passwd"
}
```

#### Output Path Validation
- **System directory protection**: Prevents writing to sensitive system directories like `/etc/`, `/sys/`, `/proc/`
- **Permission checks**: Validates write permissions before attempting to create the output file
- **Path normalization**: Removes `..` and symbolic links from paths

### Error Handling

#### Specific Exception Handling
All exception handlers use specific exception types instead of bare `except:` clauses:

```python
try:
    data = json.loads(text)
except (json.JSONDecodeError, ValueError, TypeError) as e:
    # Specific handling with logging
    print(f"Warning: {e}", file=sys.stderr)
```

#### Regular Expression DoS (ReDoS) Protection
- **Text length validation**: Regex operations are limited to text under 10 MB
- **Prevents**: Catastrophic backtracking that could freeze the program

### Data Processing

#### JSON Parsing
- **Schema validation**: Input data types are validated before processing
- **Error messages**: Clear error messages for malformed JSON
- **Type checking**: Validates expected data structures exist before accessing

```python
if not isinstance(chat_data, (dict, list)):
    raise ValueError(f"Invalid chat data format: expected object or array")
```

## Security Best Practices for Users

### When Using This Tool

1. **Trusted Sources Only**: Only process chat logs from trusted sources (your own VS Code exports)
2. **Inspect Large Files**: Before processing very large files, consider reviewing them first
3. **Output Location**: Write output files to your user directory, not system directories
4. **File Permissions**: Ensure the output directory has appropriate permissions

### Example Safe Usage

```bash
# Good: Writing to your home directory
python chat_to_markdown.py ~/Downloads/chat.json ~/Documents/chat.md

# Bad: Attempting to write to system directory (will be blocked)
python chat_to_markdown.py chat.json /etc/chat.md
```

## Known Limitations

### What This Tool Does NOT Protect Against

1. **Content Security**: The tool doesn't validate or sanitize the actual content of messages
2. **Markdown Injection**: User-provided markdown in the chat is preserved as-is
3. **External Resources**: Links in the markdown are not validated
4. **Privacy**: The tool doesn't redact sensitive information from chat logs

### User Responsibility

Users should:
- **Review output**: Check the generated markdown before sharing
- **Redact secrets**: Remove any API keys, passwords, or sensitive data from input files
- **Control access**: Restrict who can access your chat exports and generated markdown

## Security Updates

### Current Version Security Status

**Version**: 1.1.0 (as of January 2026)
**Security Level**: Hardened

Recent security improvements:
- ✅ Input validation added (v1.1.0)
- ✅ Path traversal protection (v1.1.0)
- ✅ DoS prevention (v1.1.0)
- ✅ Proper exception handling (v1.1.0)
- ✅ ReDoS protection (v1.1.0)

## Reporting a Vulnerability

### How to Report

If you discover a security vulnerability, please:

1. **DO NOT** open a public GitHub issue
2. **Email the maintainer** with details:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

3. **Wait for acknowledgment** before public disclosure

### What to Expect

- **Initial Response**: Within 48 hours
- **Status Updates**: Every 7 days until resolved
- **Fix Timeline**: Critical issues within 7 days, others within 30 days
- **Credit**: Security researchers will be credited (if desired)

### Vulnerability Severity Levels

#### Critical
- Remote code execution
- Arbitrary file system access
- Authentication bypass

#### High
- Denial of service
- Information disclosure (sensitive data)
- Privilege escalation

#### Medium
- Information disclosure (non-sensitive)
- Input validation issues
- Error handling problems

#### Low
- Best practice violations
- Documentation issues

## Security Checklist for Contributors

When contributing code, ensure:

- [ ] No bare `except:` clauses (use specific exceptions)
- [ ] All file paths are sanitized
- [ ] Input is validated before processing
- [ ] Error messages don't leak sensitive information
- [ ] Regular expressions are protected against ReDoS
- [ ] External input is never executed as code
- [ ] Dependencies are up to date (when added)

## Dependencies

### Current Dependencies

This tool uses **only the Python standard library**:
- `json` - JSON parsing
- `sys` - System operations
- `argparse` - Command-line parsing
- `os` - File system operations
- `re` - Regular expressions
- `datetime` - Timestamp formatting
- `typing` - Type hints

**No external dependencies** = Minimal attack surface!

### Dependency Security

Since we use no external dependencies:
- ✅ No supply chain attacks
- ✅ No vulnerable third-party packages
- ✅ No dependency confusion attacks
- ✅ Easier security auditing

## Compliance

### Security Standards

This project follows:
- **OWASP Top 10**: Addresses injection, broken access control, security misconfiguration
- **CWE**: Mitigates CWE-22 (Path Traversal), CWE-400 (Resource Exhaustion)
- **PEP 8**: Python coding standards for readability and maintainability

### Testing

Security features are validated through:
- Manual testing with malicious inputs
- Boundary condition testing
- Error path testing
- Integration testing with sample files

## Additional Resources

### Learning More

- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)

### Security Tools

Recommended tools for security analysis:
- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability scanner (when dependencies are added)
- **pylint**: Code quality and security checks

## License

This security policy is part of the project and follows the same MIT License.

---

**Last Updated**: January 29, 2026  
**Security Contact**: See repository owner's GitHub profile
