# Contributing to Copilot Chat to Markdown

Thank you for your interest in contributing! This document provides guidelines and best practices for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Security Guidelines](#security-guidelines)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences
- Accept responsibility and apologize for mistakes

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Git
- Text editor or IDE

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/copilot-chat-to-markdown.git
   cd copilot-chat-to-markdown
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/ZacharyLuz/copilot-chat-to-markdown.git
   ```

## Development Setup

### Basic Setup

No external dependencies are required for the main script:

```bash
# Test the script
python3 chat_to_markdown.py --help
python3 chat_to_markdown.py samples/chat.json output.md
```

### Development Tools (Optional)

Install development dependencies for linting, formatting, and testing:

```bash
pip install -r requirements-dev.txt
```

This includes:
- `black` - Code formatting
- `pylint` - Code linting
- `flake8` - Style checking
- `mypy` - Type checking
- `bandit` - Security scanning
- `pytest` - Testing framework
- `pre-commit` - Git hooks

### Pre-commit Hooks

Set up pre-commit hooks to automatically check code before committing:

```bash
pre-commit install
```

Run manually on all files:

```bash
pre-commit run --all-files
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://peps.python.org/pep-0008/) with these specifics:

- **Line length**: 120 characters maximum
- **Indentation**: 4 spaces (no tabs)
- **Imports**: Grouped at the top of the file
  - Standard library imports first
  - Third-party imports second (if any)
  - Local imports last
- **Naming conventions**:
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

### Code Formatting

Use Black for consistent formatting:

```bash
black --line-length 120 chat_to_markdown.py
```

### Documentation

- Add docstrings to all functions using this format:
  ```python
  def function_name(param1: type1, param2: type2) -> return_type:
      """
      Brief description of what the function does.
      
      Args:
          param1: Description of param1
          param2: Description of param2
          
      Returns:
          Description of return value
          
      Raises:
          ExceptionType: When this exception is raised
      """
  ```

- Keep comments clear and concise
- Update documentation when changing functionality

### Type Hints

Use type hints for function parameters and return values:

```python
from typing import Dict, List, Any, Optional

def process_data(data: Dict[str, Any]) -> Optional[str]:
    # Function implementation
    pass
```

## Security Guidelines

### Critical Security Rules

1. **Never use bare `except:` clauses**
   ```python
   # Bad
   try:
       risky_operation()
   except:
       pass
   
   # Good
   try:
       risky_operation()
   except (ValueError, TypeError) as e:
       print(f"Error: {e}", file=sys.stderr)
   ```

2. **Always validate input**
   ```python
   # Validate file sizes
   if os.path.getsize(filepath) > MAX_SIZE:
       raise ValueError("File too large")
   
   # Validate types
   if not isinstance(data, dict):
       raise TypeError("Expected dict")
   ```

3. **Sanitize file paths**
   ```python
   # Use the sanitize_file_path function
   safe_path = sanitize_file_path(user_input)
   ```

4. **Protect against ReDoS**
   ```python
   # Check text length before regex
   if len(text) > MAX_TEXT_LENGTH:
       raise ValueError("Text too long")
   ```

5. **No external code execution**
   - Never use `eval()`, `exec()`, or similar
   - Be careful with `subprocess` calls
   - Validate all user input

### Security Checklist

Before submitting code, verify:

- [ ] No bare exception handlers
- [ ] All file paths are sanitized
- [ ] Input is validated before processing
- [ ] Regular expressions are protected against ReDoS
- [ ] Error messages don't leak sensitive information
- [ ] No hardcoded secrets or credentials

### Running Security Scans

```bash
# Run Bandit security scanner
bandit -r . -c pyproject.toml

# Check for common issues
pylint chat_to_markdown.py
```

## Testing

### Manual Testing

Test your changes with the sample file:

```bash
python3 chat_to_markdown.py samples/chat.json /tmp/output.md
```

### Test Security Features

```python
# Test file size validation
python3 -c "
from chat_to_markdown import validate_file_size
validate_file_size('samples/chat.json')
print('✓ File size validation works')
"

# Test path sanitization
python3 -c "
from chat_to_markdown import sanitize_file_path
result = sanitize_file_path('../../etc/passwd')
assert result == 'passwd', f'Expected passwd, got {result}'
print('✓ Path sanitization works')
"
```

### Edge Cases to Test

- Empty JSON files
- Very large files (near the 100 MB limit)
- Malformed JSON
- Missing required fields
- Special characters in file paths
- Unicode content

## Submitting Changes

### Branch Naming

Use descriptive branch names:

- `feature/add-xyz` - New features
- `fix/issue-123` - Bug fixes
- `security/cve-xyz` - Security fixes
- `docs/update-readme` - Documentation updates

### Commit Messages

Follow these guidelines:

- Use present tense: "Add feature" not "Added feature"
- Be descriptive but concise
- Reference issues: "Fix #123: Handle empty JSON files"
- Separate subject from body with a blank line

Example:
```
Add input validation for file size

- Implement MAX_FILE_SIZE_BYTES constant
- Add validate_file_size function
- Update main() to check file size before loading
- Prevents DoS attacks from extremely large files

Fixes #123
```

### Pull Request Process

1. **Update your fork**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Create a pull request**:
   - Provide a clear title and description
   - Reference related issues
   - Include test results
   - Add before/after examples if applicable

3. **PR Checklist**:
   - [ ] Code follows style guidelines
   - [ ] All tests pass
   - [ ] Security checks pass
   - [ ] Documentation is updated
   - [ ] Commit messages are clear
   - [ ] No sensitive data in commits

4. **Review process**:
   - Maintainers will review your PR
   - Address feedback and comments
   - Make requested changes
   - Ensure CI checks pass

### What Happens Next

- **Review time**: Usually within 7 days
- **Feedback**: Maintainers may request changes
- **Merge**: Once approved, your PR will be merged
- **Credit**: You'll be credited in the commit and release notes

## Areas for Contribution

### High Priority

- Unit tests for critical functions
- Integration tests
- Performance improvements
- Documentation improvements

### Medium Priority

- Support for additional chat formats
- Output format options (HTML, PDF)
- Better error messages
- Localization/internationalization

### Low Priority

- UI/CLI improvements
- Additional output customization
- Performance profiling tools

## Questions?

- Open an issue for questions
- Tag with "question" label
- Check existing issues first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be:
- Listed in release notes
- Credited in commit messages
- Added to a CONTRIBUTORS file (if created)

Thank you for contributing! 🎉
