# Contributing to PDFForge

Thank you for your interest in contributing to PDFForge! 

## Code of Conduct

By participating in this project, you agree to maintain a welcoming and respectful environment for everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Create a detailed issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Sample PDF file (if possible)

### Suggesting Features

1. Check existing issues for similar suggestions
2. Open a new issue with:
   - Clear title and description
   - Use case explanation
   - Example usage (if applicable)

### Pull Requests

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes:
   - Write clear, commented code
   - Follow existing code style
   - Add tests if applicable

4. Commit your changes:
   ```bash
   git commit -m "feat: add your feature description"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Open a Pull Request

### Commit Message Format

We follow Conventional Commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/gitstq/PDFForge.git
   cd PDFForge
   ```

2. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

3. Run tests:
   ```bash
   pytest tests/ -v
   ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for public functions
- Keep lines under 100 characters

## Questions?

Feel free to open an issue for any questions!
