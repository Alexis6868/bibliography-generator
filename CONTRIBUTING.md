# Contributing to Bibliography Generator

We welcome contributions! Here's how you can help.

## Educational Context

This is an **academic Computer Science project (SY48)** created for educational purposes.
Contributions should align with the educational objectives and maintain code quality standards.

## Development Setup

```bash
# Clone the repository
git clone <repository>
cd bibliography-generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
make install-dev
```

## Running Tests

```bash
# Run all tests
make test

# Run specific test suites
make test-features
make test-cli

# Generate coverage report
make test-coverage
```

## Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Run type checking
make type-check
```

## Common Commands

```bash
# Run example
make example

# View documentation
make docs

# Clean up generated files
make clean
make clean-db
```

## Project Structure

```
src/
├── core/          # Lexer, Parser, Generator
├── features/      # Citation formatters
├── utils/         # Database, ML extraction, i18n
├── main.py        # Basic CLI
└── enhanced_main.py # Full-featured CLI

tests/
├── test_features.py
├── test_parser.py
└── sample_input.txt

docs/             # Complete documentation
```

## Code Style

- Use type hints for all functions
- Follow PEP 8 (enforced with black/flake8)
- Add docstrings to all modules and classes
- Write tests for new features

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Run `make test` and `make lint`
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Reporting Issues

- Use the issue tracker
- Include steps to reproduce
- Provide Python version and OS information
- Attach example files if applicable

## License

By contributing, you agree your contributions will be licensed under the Educational License
for Academic Use. See [LICENSE](LICENSE) file for details.

Contributions should respect the educational nature of this project and maintain proper
attribution of ideas and code sources.

---

Thank you for contributing! 🎉
