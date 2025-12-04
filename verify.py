#!/usr/bin/env python3
"""
Project Verification Script
Ensures everything is working correctly and ready to use
"""

import os
import sys
from pathlib import Path

def check_structure():
    """Check project structure"""
    print("📁 Checking Project Structure...")
    
    required_dirs = [
        "src/core",
        "src/features", 
        "src/utils",
        "bin",
        "tests",
        "output",
        "docs"
    ]
    
    required_files = [
        "src/core/lexer.py",
        "src/core/parser.py",
        "src/core/generator.py",
        "src/features/formatters.py",
        "src/utils/ml_extractor.py",
        "src/utils/database.py",
        "src/utils/i18n.py",
        "bin/bibliography",
        "README.md",
    ]
    
    all_good = True
    
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/ NOT FOUND")
            all_good = False
    
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} NOT FOUND")
            all_good = False
    
    return all_good

def check_docs():
    """Check documentation"""
    print("\n📚 Checking Documentation...")
    
    docs_required = [
        "docs/QUICK_START.md",
        "docs/INSTALLATION.md",
        "docs/API_REFERENCE.md",
        "docs/TROUBLESHOOTING.md",
        "docs/PROJECT_STRUCTURE.md",
    ]
    
    all_good = True
    for doc in docs_required:
        if os.path.isfile(doc):
            print(f"  ✓ {doc}")
        else:
            print(f"  ✗ {doc} NOT FOUND")
            all_good = False
    
    return all_good

def check_tests():
    """Check test files"""
    print("\n🧪 Checking Tests...")
    
    test_files = [
        "tests/test_parser.py",
        "tests/test_features.py",
        "tests/sample_input.txt",
    ]
    
    all_good = True
    for test in test_files:
        if os.path.isfile(test):
            print(f"  ✓ {test}")
        else:
            print(f"  ✗ {test} NOT FOUND")
            all_good = False
    
    return all_good

def check_imports():
    """Check Python imports work"""
    print("\n🐍 Checking Python Imports...")
    
    try:
        from src.core.lexer import OptimizedLexer
        print("  ✓ src.core.lexer")
    except Exception as e:
        print(f"  ✗ src.core.lexer: {e}")
        return False
    
    try:
        from src.core.parser import OptimizedParser
        print("  ✓ src.core.parser")
    except Exception as e:
        print(f"  ✗ src.core.parser: {e}")
        return False
    
    try:
        from src.core.generator import OptimizedBibTeXGenerator
        print("  ✓ src.core.generator")
    except Exception as e:
        print(f"  ✗ src.core.generator: {e}")
        return False
    
    try:
        from src.features.formatters import FormattersFactory
        print("  ✓ src.features.formatters")
    except Exception as e:
        print(f"  ✗ src.features.formatters: {e}")
        return False
    
    try:
        from src.utils.ml_extractor import MLFieldExtractor
        print("  ✓ src.utils.ml_extractor")
    except Exception as e:
        print(f"  ✗ src.utils.ml_extractor: {e}")
        return False
    
    try:
        from src.utils.database import BibliographyDatabase
        print("  ✓ src.utils.database")
    except Exception as e:
        print(f"  ✗ src.utils.database: {e}")
        return False
    
    try:
        from src.utils.i18n import I18nManager
        print("  ✓ src.utils.i18n")
    except Exception as e:
        print(f"  ✗ src.utils.i18n: {e}")
        return False
    
    return True

def check_sample():
    """Check sample functionality"""
    print("\n🚀 Checking Sample Functionality...")
    
    try:
        from src.core.parser import OptimizedParser
        from src.core.generator import OptimizedBibTeXGenerator
        
        parser = OptimizedParser()
        generator = OptimizedBibTeXGenerator()
        
        # Test parse
        text = "Smith et al. 2023. A study. Nature 45: 1-10"
        entry = parser.parse(text)
        
        if not entry.title:
            print("  ✗ Parser failed to extract title")
            return False
        
        print(f"  ✓ Parser: extracted '{entry.title[:30]}...'")
        
        # Test generate
        from src.core.generator import BibEntry
        bib_entry = BibEntry(
            entry_id="test1",
            entry_type="article",
            authors=entry.authors,
            title=entry.title,
            year=entry.year,
            journal=entry.journal,
            volume=entry.volume,
            pages=entry.pages
        )
        
        output = generator.generate(bib_entry)
        
        if "@article" not in output:
            print("  ✗ Generator failed to generate BibTeX")
            return False
        
        print("  ✓ Generator: created BibTeX entry")
        return True
        
    except Exception as e:
        print(f"  ✗ Sample test failed: {e}")
        return False

def main():
    """Run all checks"""
    print("═" * 60)
    print("BIBLIOGRAPHY GENERATOR - PROJECT VERIFICATION")
    print("═" * 60)
    
    checks = [
        ("Project Structure", check_structure),
        ("Documentation", check_docs),
        ("Tests", check_tests),
        ("Python Imports", check_imports),
        ("Sample Functionality", check_sample),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} check failed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✨ ALL CHECKS PASSED! ✨")
        print("\nYour project is ready to use!")
        print("\nNext steps:")
        print("  1. Read docs/QUICK_START.md")
        print("  2. Run: python bin/bibliography tests/sample_input.txt output/test.bib")
        print("  3. Check: cat output/test.bib")
        print("=" * 60)
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("Please review the errors above.")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
