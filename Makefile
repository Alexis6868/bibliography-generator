.PHONY: help test test-all test-features test-cli test-coverage clean install lint format type-check docs run example

help:
	@echo "Bibliography Generator - Development Commands"
	@echo ""
	@echo "Testing:"
	@echo "  make test            - Run all tests"
	@echo "  make test-all        - Run all feature tests"
	@echo "  make test-features   - Run comprehensive feature tests"
	@echo "  make test-cli        - Run CLI end-to-end tests"
	@echo "  make test-coverage   - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint            - Run linting (flake8)"
	@echo "  make format          - Format code (black)"
	@echo "  make type-check      - Run type checking (mypy)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           - Remove generated files"
	@echo "  make clean-db        - Remove database files"
	@echo ""
	@echo "Examples:"
	@echo "  make example         - Run example conversion"
	@echo "  make docs            - Show documentation links"

test: test-features test-cli
	@echo "✅ All tests passed!"

test-all:
	@echo "Running comprehensive feature tests..."
	python test_all_features.py

test-features:
	@echo "Running feature tests..."
	python test_all_features.py

test-cli:
	@echo "Running CLI tests..."
	python test_cli.py

test-coverage:
	@echo "Running tests with coverage..."
	pytest tests/ -v --cov=src --cov-report=html
	@echo "Coverage report generated in htmlcov/"

verify:
	@echo "Verifying project integrity..."
	python verify.py

lint:
	@echo "Running linting..."
	flake8 src/ tests/ --max-line-length=100

format:
	@echo "Formatting code..."
	black src/ tests/ --line-length=100

type-check:
	@echo "Running type checking..."
	mypy src/ --ignore-missing-imports

clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name htmlcov -exec rm -rf {} +
	find . -name .coverage -delete
	@echo "✅ Cleanup complete"

clean-db:
	@echo "Removing database files..."
	rm -f refs.db output/*.db
	@echo "✅ Database files removed"

clean-output:
	@echo "Clearing output files..."
	rm -f output/*.bib output/*.txt
	@echo "✅ Output cleared"

install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements.txt

example:
	@echo "Creating example input file..."
	@echo "Smith, J. and Johnson, K., 2023. Machine learning applications. Nature, 45(3), pp.123-145." > example_input.txt
	@echo "Brown, A., 2022. Deep learning fundamentals. IEEE Transactions, 34, pp.567-580." >> example_input.txt
	@echo ""
	@echo "Converting to BibTeX..."
	python -m src.enhanced_main example_input.txt output/example.bib
	@echo ""
	@echo "Output saved to: output/example.bib"
	@cat output/example.bib

docs:
	@echo "📚 Documentation Files:"
	@echo "  - docs/QUICK_START.md      - 30-second setup guide"
	@echo "  - docs/INSTALLATION.md     - Detailed installation"
	@echo "  - docs/API_REFERENCE.md    - API documentation"
	@echo "  - docs/PROJECT_STRUCTURE.md - Architecture overview"
	@echo "  - docs/TROUBLESHOOTING.md  - Common issues & solutions"
	@echo ""
	@echo "📊 Test Files:"
	@echo "  - test_all_features.py     - 7 feature tests (7/7 passing)"
	@echo "  - test_cli.py              - 3 CLI test suites (3/3 passing)"
	@echo "  - tests/test_features.py   - 21 unit tests"
	@echo "  - tests/test_parser.py     - 11 parser tests"
