# Contributing to Deep Research Python

Thank you for your interest in contributing to Deep Research Python! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment:
   ```bash
   make install
   make setup-env
   ```
4. Edit the `.env` file with your API keys
5. Test your setup:
   ```bash
   make test-setup
   ```

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation
```bash
git clone https://github.com/your-username/deep-research-python.git
cd deep-research-python
make install
```

### Running Tests
```bash
make test-setup  # Test AI provider configuration
make test        # Run full test suite (when available)
```

## Code Style

This project follows Python PEP 8 style guidelines. We use:
- `black` for code formatting
- `flake8` for linting

Run the linters:
```bash
make lint        # Check code style
make format      # Auto-format code
```

## Making Changes

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following these guidelines:
   - Write clear, concise commit messages
   - Add docstrings to new functions and classes
   - Update the README.md if you're adding new features
   - Add tests for new functionality

3. Test your changes:
   ```bash
   make test-setup
   python main.py "test query"
   ```

4. Submit a pull request with:
   - Clear description of the changes
   - Any breaking changes noted
   - Steps to test the changes

## Areas for Contribution

- **New AI Providers**: Add support for additional AI services
- **Search Engines**: Integrate with more search providers
- **Output Formats**: Add support for different report formats
- **Performance**: Optimize search and processing speed
- **Testing**: Add comprehensive test coverage
- **Documentation**: Improve documentation and examples

## Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Error messages and stack traces
- Steps to reproduce the issue
- Expected vs actual behavior

## Code of Conduct

Please be respectful and constructive in all interactions. This project welcomes contributions from everyone, regardless of background or experience level.

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License. 