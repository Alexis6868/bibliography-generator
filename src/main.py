"""
Main entry point for Bibliography Generator.
Provides basic interface for bibliography processing.
"""

import sys
import argparse
from typing import List

from src.core.parser import OptimizedParser
from src.core.generator import OptimizedBibTeXGenerator


class BibliographyGenerator:
    """Main controller for bibliography generation pipeline."""
    
    def __init__(self):
        """Initialize generator with optimized components."""
        self.parser = OptimizedParser()
        self.generator = OptimizedBibTeXGenerator()
        self.entries = []
    
    def process_text(self, text: str, entry_id: str = None):
        """Process a single bibliography reference."""
        entry = self.parser.parse(text, entry_id)
        self.entries.append(entry)
        return entry
    
    def process_file(self, filepath: str) -> List:
        """Process bibliography references from a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            references = content.strip().split('\n')
            
            for idx, ref in enumerate(references, 1):
                ref = ref.strip()
                if ref and not ref.startswith('#'):
                    self.process_text(ref, f"ID{idx}")
            
            return self.entries
        
        except FileNotFoundError:
            print(f"✗ Error: File '{filepath}' not found.")
            return []
        except Exception as e:
            print(f"✗ Error processing file: {e}")
            return []
    
    def output_bibtex(self, filepath: str = None) -> str:
        """Output BibTeX format."""
        output = self.generator.generate_batch(self.entries)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✓ Output written to: {filepath}")
        
        return output
    
    def clear(self):
        """Clear processed entries."""
        self.entries.clear()
        self.parser.clear_cache()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Bibliography Generator - Convert text to BibTeX",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main input.txt output.bib
  python -m src.main refs.txt -o output.bib
        """
    )
    
    parser.add_argument('input_file', help='Input file with references')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    
    args = parser.parse_args()
    
    gen = BibliographyGenerator()
    entries = gen.process_file(args.input_file)
    
    if not entries:
        print("✗ No references processed")
        sys.exit(1)
    
    print(f"✓ Processed {len(entries)} references")
    
    if args.output:
        gen.output_bibtex(args.output)
    else:
        print(gen.output_bibtex())


if __name__ == "__main__":
    main()
