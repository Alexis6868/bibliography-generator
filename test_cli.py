#!/usr/bin/env python3
"""
CLI End-to-End Test Suite
Tests the enhanced_main.py CLI with all features
"""

import subprocess
import os
import sys
from pathlib import Path

def run_command(cmd):
    """Run a command and return output"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def test_cli_formats():
    """Test CLI with different formats"""
    print("\n" + "="*60)
    print("TEST: CLI with Different Formats")
    print("="*60)
    
    # Create test input
    test_input = """Smith, J. and Johnson, K., 2023. Machine learning applications. Nature, 45(3), pp.123-145.
    Brown, A., 2022. Deep learning fundamentals. IEEE Transactions, 34, pp.567-580.
    Davis, C., 2021. Neural networks survey. Journal of AI, 12(1), pp.89-102."""
    
    with open("test_input_cli.txt", "w") as f:
        f.write(test_input)
    
    formats = ['bibtex', 'ieee', 'apa', 'chicago', 'mla']
    results = []
    
    for fmt in formats:
        print(f"\nTesting format: {fmt}")
        cmd = f"python3 -m src.enhanced_main test_input_cli.txt output/test_{fmt}.bib --format {fmt}"
        
        returncode, stdout, stderr = run_command(cmd)
        
        if returncode == 0:
            # Check if output file was created
            output_file = f"output/test_{fmt}.bib"
            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"  ✓ {fmt.upper()}: Success ({size} bytes)")
                with open(output_file, 'r') as f:
                    content = f.read()
                    print(f"    Sample: {content[:100]}...")
                results.append((fmt, True))
            else:
                print(f"  ✗ {fmt.upper()}: Output file not created")
                results.append((fmt, False))
        else:
            print(f"  ✗ {fmt.upper()}: Failed")
            print(f"    Error: {stderr}")
            results.append((fmt, False))
    
    # Cleanup
    os.remove("test_input_cli.txt")
    
    # Summary
    passed = sum(1 for _, success in results if success)
    print(f"\n✓ Format tests: {passed}/{len(formats)} passed")
    
    return passed == len(formats)

def test_cli_languages():
    """Test CLI with different languages"""
    print("\n" + "="*60)
    print("TEST: CLI with Different Languages")
    print("="*60)
    
    # Create test input
    test_input = "Smith, J., 2023. Study. Nature, 45, pp.1-10."
    
    with open("test_input_lang.txt", "w") as f:
        f.write(test_input)
    
    languages = ['en', 'fr', 'es', 'de', 'zh']
    results = []
    
    for lang in languages:
        print(f"\nTesting language: {lang}")
        cmd = f"python3 -m src.enhanced_main test_input_lang.txt output/test_{lang}.bib --language {lang}"
        
        returncode, stdout, stderr = run_command(cmd)
        
        if returncode == 0:
            output_file = f"output/test_{lang}.bib"
            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"  ✓ {lang.upper()}: Success ({size} bytes)")
                results.append((lang, True))
            else:
                print(f"  ✗ {lang.upper()}: Output file not created")
                results.append((lang, False))
        else:
            print(f"  ✗ {lang.upper()}: Failed")
            print(f"    Error: {stderr}")
            results.append((lang, False))
    
    # Cleanup
    os.remove("test_input_lang.txt")
    
    # Summary
    passed = sum(1 for _, success in results if success)
    print(f"\n✓ Language tests: {passed}/{len(languages)} passed")
    
    return passed == len(languages)

def test_cli_quality():
    """Test CLI with quality options"""
    print("\n" + "="*60)
    print("TEST: CLI with Quality Analysis")
    print("="*60)
    
    test_input = "Smith, J., 2023. Study. Nature, 45, pp.1-10."
    
    with open("test_input_quality.txt", "w") as f:
        f.write(test_input)
    
    cmd = "python3 -m src.enhanced_main test_input_quality.txt output/quality_test.bib --quality"
    
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode == 0:
        print(f"✓ Quality analysis: Success")
        print(f"  Output:\n{stdout}")
        os.remove("test_input_quality.txt")
        return True
    else:
        print(f"✗ Quality analysis: Failed")
        print(f"  Error: {stderr}")
        os.remove("test_input_quality.txt")
        return False

def main():
    """Run all CLI tests"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " CLI END-TO-END TEST ".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Run tests
    test_results = {
        "Formats": test_cli_formats(),
        "Languages": test_cli_languages(),
        "Quality": test_cli_quality(),
    }
    
    # Summary
    print("\n" + "="*60)
    print("CLI TEST SUMMARY")
    print("="*60)
    
    for name, success in test_results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{name:.<40} {status}")
    
    passed = sum(1 for v in test_results.values() if v)
    total = len(test_results)
    
    print("\n" + "="*60)
    print(f"RESULT: {passed}/{total} test suites passed")
    print("="*60)
    
    if passed == total:
        print("\n✓ All CLI tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test suite(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
