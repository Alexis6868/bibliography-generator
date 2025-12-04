# Troubleshooting Guide

## Installation Issues

### Issue: "ModuleNotFoundError: No module named 'src'"

**Cause**: Running from wrong directory

**Solution**:
```bash
# Make sure you're in the project root
cd PROJET
python bin/bibliography tests/sample_input.txt output/test.bib
```

### Issue: "python: command not found"

**Cause**: Python not installed or not in PATH

**Solution**:
```bash
# Check if Python is installed
python --version

# If not found, install Python:
# macOS: brew install python3
# Linux: apt-get install python3
# Windows: Download from python.org
```

### Issue: "No such file or directory"

**Cause**: Input file doesn't exist

**Solution**:
```bash
# Check if file exists
ls tests/sample_input.txt

# Or create output directory
mkdir -p output
```

---

## Runtime Issues

### Issue: "PermissionError: [Errno 13] Permission denied"

**Cause**: Script doesn't have execute permissions (macOS/Linux)

**Solution**:
```bash
chmod +x bin/bibliography
python bin/bibliography tests/sample_input.txt output/test.bib
```

### Issue: Output file is empty

**Cause**: Invalid input format

**Solution**:
```bash
# Check input file format
cat tests/sample_input.txt

# Entries should be separated by blank lines
# Example: "Author. Title. Journal, year"

# Verify with sample
python bin/bibliography tests/sample_input.txt output/test.bib
```

### Issue: Encoding error with special characters

**Cause**: File encoding issue

**Solution**:
```bash
# Ensure input file is UTF-8
file tests/sample_input.txt

# If not UTF-8, convert it:
iconv -f ISO-8859-1 -t UTF-8 input.txt > input_utf8.txt
```

---

## Performance Issues

### Issue: Processing is slow

**Cause**: Not using batch processing or caching

**Solution**:
```python
# ✗ Slow - processes each entry separately
for ref in references:
    output += generator.generate(parser.parse(ref))

# ✓ Fast - batch processing with cache
entries = [parser.parse(ref, use_cache=True) for ref in references]
output = generator.generate_batch(entries)
```

### Issue: High memory usage

**Cause**: Parser cache is too large

**Solution**:
```python
# Clear cache periodically
parser.clear_cache()

# Or process in batches
for batch in chunks(references, 100):
    entries = [parser.parse(ref, use_cache=True) for ref in batch]
    output = generator.generate_batch(entries)
```

---

## Format Issues

### Issue: Format not recognized

**Cause**: Invalid format name

**Solution**:
```bash
# Use one of these formats:
python bin/bibliography input.txt output.bib --format bibtex
python bin/bibliography input.txt output.bib --format ieee
python bin/bibliography input.txt output.bib --format apa
python bin/bibliography input.txt output.bib --format chicago
python bin/bibliography input.txt output.bib --format mla

# Default is bibtex if not specified
```

### Issue: Formatting looks wrong

**Cause**: Missing fields in input

**Solution**:
```bash
# Ensure input has key fields:
# Author, Title, Journal/Publisher, Year, Volume/Pages

# Example good input:
Smith, J., Johnson, K. A Study. Nature, vol. 45, pp. 1-10, 2023.

# Example poor input (will be incomplete):
Smith. Some text.
```

---

## Language Issues

### Issue: Language not recognized

**Cause**: Invalid language code

**Solution**:
```bash
# Use one of these language codes:
python bin/bibliography input.txt output.bib --language en
python bin/bibliography input.txt output.bib --language fr
python bin/bibliography input.txt output.bib --language es
python bin/bibliography input.txt output.bib --language de
python bin/bibliography input.txt output.bib --language zh

# Default is en if not specified
```

### Issue: Characters display incorrectly

**Cause**: Terminal encoding issue

**Solution**:
```bash
# Set terminal to UTF-8
export LANG=en_US.UTF-8
python bin/bibliography input.txt output.bib --language zh
```

---

## Database Issues

### Issue: "Database is locked"

**Cause**: Multiple processes accessing database simultaneously

**Solution**:
```python
# Wait for lock to be released
import time
time.sleep(1)
db = BibliographyDatabase("bib.db")

# Or use different database file for each process
db = BibliographyDatabase(f"bib_{process_id}.db")
```

### Issue: "No such table"

**Cause**: Database file corrupted or not initialized

**Solution**:
```bash
# Delete corrupted database
rm bibliography.db

# It will be recreated automatically
python bin/bibliography input.txt output.bib
```

---

## Testing Issues

### Issue: "pytest: command not found"

**Cause**: pytest not installed

**Solution**:
```bash
# Install pytest (optional, only for testing)
pip install pytest pytest-cov

# Then run tests
python -m pytest tests/ -v
```

### Issue: Tests fail with import errors

**Cause**: Wrong Python path

**Solution**:
```bash
# Run from project root
cd PROJET
python -m pytest tests/ -v
```

### Issue: "ImportError: No module named 'src'"

**Cause**: Running from wrong directory

**Solution**:
```bash
# Make sure you're in project root
cd PROJET
python -m pytest tests/ -v
```

---

## Import Issues

### Issue: "No module named 'src.core'"

**Cause**: Python path not set correctly

**Solution**:
```bash
# Run from project root directory
cd PROJET

# Then run commands
python bin/bibliography tests/sample_input.txt output/test.bib

# Or add to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/PROJET"
```

### Issue: "circular import error"

**Cause**: Module import order issue

**Solution**:
```python
# This is already fixed in the code
# If you modify imports, ensure no circular dependencies:

# Good:
from src.core.lexer import OptimizedLexer
from src.features.formatters import FormattersFactory

# Avoid circular imports
```

---

## Output Issues

### Issue: Output file not created

**Cause**: Output directory doesn't exist

**Solution**:
```bash
# Create output directory
mkdir -p output

# Then run
python bin/bibliography input.txt output/test.bib
```

### Issue: Output file is incomplete

**Cause**: Process interrupted or input invalid

**Solution**:
```bash
# Verify input file
cat input.txt

# Check file size
wc -l input.txt

# Try with sample
python bin/bibliography tests/sample_input.txt output/test.bib
```

---

## Command Line Issues

### Issue: "unrecognized arguments"

**Cause**: Wrong argument format

**Solution**:
```bash
# Correct format:
python bin/bibliography INPUT OUTPUT [--format FORMAT] [--language LANG]

# Examples:
python bin/bibliography input.txt output.bib
python bin/bibliography input.txt output.bib --format ieee
python bin/bibliography input.txt output.bib --language fr
python bin/bibliography input.txt output.bib --format ieee --language fr
```

### Issue: Help not showing

**Solution**:
```bash
python bin/bibliography --help
```

---

## System-Specific Issues

### macOS
```bash
# Use python3 explicitly
python3 --version
python3 bin/bibliography input.txt output.bib

# Or create alias
alias python=python3
```

### Windows
```bash
# Use py command
py --version
py bin/bibliography input.txt output.bib

# Or use full path
C:\Python3\python.exe bin/bibliography input.txt output.bib
```

### Linux
```bash
# Usually python3 is needed
python3 --version
python3 bin/bibliography input.txt output.bib
```

---

## Debug Mode

### Enable Debug Output

```python
import sys

# Add debug tracing
def debug_parse(text):
    from src.core.parser import OptimizedParser
    parser = OptimizedParser()
    entry = parser.parse(text)
    print(f"Parsed: {entry.title}")
    print(f"Year: {entry.year}")
    print(f"Journal: {entry.journal}")
    return entry

debug_parse("Smith et al. 2023. Study. Nature 45: 1-10")
```

### Verbose Mode

```bash
# Add -v for verbose output
python -m pytest tests/ -v -s

# Add debug logging
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from src.core.parser import OptimizedParser
p = OptimizedParser()
entry = p.parse('Smith 2023. Study. Nature')
print(entry)
"
```

---

## Getting Help

1. **Check sample**: `python bin/bibliography tests/sample_input.txt output/test.bib`
2. **Read docs**: See `docs/` folder
3. **Check tests**: See `tests/` folder for examples
4. **Review code**: Comments in `src/` modules

---

## Report Issues

Include:
- Operating system
- Python version: `python --version`
- Error message (full traceback)
- Input file (if possible)
- Command used

---

**Version**: 2.0
**Status**: Production Ready ✓
**Last Updated**: 2024
