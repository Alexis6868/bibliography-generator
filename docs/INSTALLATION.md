# Installation Guide

## System Requirements

- **Python**: 3.7 or higher
- **OS**: macOS, Linux, or Windows
- **Storage**: ~50MB
- **Dependencies**: None (pure Python, uses only standard library)

## Quick Start (3 steps)

### 1. Clone or Navigate to Project
```bash
cd PROJET
```

### 2. Verify Python Installation
```bash
python --version
# Should show Python 3.7+
```

### 3. Run Your First Bibliography
```bash
python bin/bibliography tests/sample_input.txt output/first.bib
```

Done! Your bibliography is in `output/first.bib`

---

## Detailed Installation

### Option A: Direct Usage (No Setup Required)

The project works immediately after download. No installation or virtual environment needed.

```bash
# Navigate to project
cd PROJET

# Run directly
python bin/bibliography <input> <output>
```

### Option B: Virtual Environment (Recommended)

Create an isolated environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify it's active (you should see (venv) in prompt)

# Ready to use!
python bin/bibliography tests/sample_input.txt output/test.bib
```

### Option C: Development Setup

If modifying code:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install testing tools (optional)
pip install pytest pytest-cov

# Run tests
python -m pytest tests/ -v
```

---

## Verify Installation

### Test 1: Check Python Version
```bash
python --version
```
Should output Python 3.7+

### Test 2: Test Basic Import
```bash
python -c "from src.core.lexer import OptimizedLexer; print('✓ Lexer OK')"
```

### Test 3: Run Sample
```bash
python bin/bibliography tests/sample_input.txt output/verify.bib
cat output/verify.bib
```

### Test 4: Run All Tests (if pytest installed)
```bash
python -m pytest tests/ -v
```

Expected output: **32/32 tests passing**

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution**: Make sure you're running from the project root:
```bash
cd PROJET
python bin/bibliography tests/sample_input.txt output/test.bib
```

### Issue: "Python not found"

**Solution**: Install Python from [python.org](https://www.python.org)

### Issue: File not found errors

**Solution**: Create the `output` folder:
```bash
mkdir -p output
```

### Issue: "pytest not found"

**Solution**: pytest is optional for basic usage. Only needed for testing:
```bash
pip install pytest pytest-cov
```

### Issue: Permission denied on macOS/Linux

**Solution**: Make script executable:
```bash
chmod +x bin/bibliography
```

---

## What's Installed

✓ **No external dependencies** - Uses only Python standard library
✓ **No virtual environment required** - Can run directly
✓ **Fully functional** - All features work immediately
✓ **Test-ready** - 32 tests included
✓ **Well-documented** - Comprehensive guides provided

---

## First Run Checklist

- [ ] Python 3.7+ installed
- [ ] Navigate to `PROJET` folder
- [ ] Run: `python bin/bibliography tests/sample_input.txt output/test.bib`
- [ ] Check: `cat output/test.bib`
- [ ] Success: Bibliography file created ✓

---

## Next Steps

1. **Try different formats**:
   ```bash
   python bin/bibliography tests/sample_input.txt output/ieee.bib --format ieee
   ```

2. **Try different languages**:
   ```bash
   python bin/bibliography tests/sample_input.txt output/fr.bib --language fr
   ```

3. **Run the tests**:
   ```bash
   python -m pytest tests/ -v
   ```

4. **Read the usage guide**: See `USAGE.md`

---

## System-Specific Notes

### macOS
- Python usually pre-installed (may be Python 2.x)
- Install Python 3: `brew install python3`
- Use `python3` instead of `python`

### Linux
- Install Python: `apt-get install python3`
- Usually already available

### Windows
- Download from [python.org](https://www.python.org)
- Add Python to PATH during installation
- Use `python` or `py` command

---

**Version**: 2.0
**Status**: Production Ready ✓
**Last Updated**: 2024
