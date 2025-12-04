#!/usr/bin/env python3
"""
Enhanced main module with all new features.
Demonstrates usage of formatters, ML extraction, database, i18n.
"""

import sys
import argparse
from typing import List

from src.core.parser import OptimizedParser
from src.core.generator import OptimizedBibTeXGenerator
from src.features.formatters import FormattersFactory
from src.utils.ml_extractor import MLFieldExtractor, QualityAssurance
from src.utils.database import BibliographyDatabase
from src.utils.i18n import I18nManager, Language


class EnhancedBibliographyGenerator:
    """Enhanced bibliography generator with all features."""
    
    def __init__(self, language: Language = Language.EN):
        """Initialize generator."""
        self.parser = OptimizedParser()
        self.generator = OptimizedBibTeXGenerator()
        self.ml_extractor = MLFieldExtractor()
        self.qa = QualityAssurance()
        self.i18n = I18nManager()  # Singleton - set language via set_language()
        self.i18n.set_language(language)
        self.entries = []
        self.db = None
    
    def set_database(self, db_path: str = None):
        """Set up database."""
        self.db = BibliographyDatabase(db_path)
    
    def process_file(self, filepath: str) -> List:
        """Process bibliography file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse references (one per line)
            references = content.strip().split('\n')
            
            for idx, ref in enumerate(references, 1):
                ref = ref.strip()
                if ref and not ref.startswith('#'):
                    entry = self.parser.parse(ref, f"ID{idx}")
                    self.entries.append(entry)
                    
                    # Store in database if available
                    if self.db:
                        self.db.add_entry(
                            entry.entry_id,
                            entry.entry_type,
                            author=entry.authors,
                            title=entry.title,
                            journal=entry.journal,
                            year=entry.year,
                            volume=entry.volume,
                            pages=entry.pages
                        )
            
            print(f"✓ Processed {len(self.entries)} references")
            return self.entries
        
        except FileNotFoundError:
            print(f"✗ Error: {filepath} not found")
            return []
    
    def output_bibtex(self, filepath: str = None) -> str:
        """Output BibTeX format."""
        output = self.generator.generate_batch(self.entries)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✓ BibTeX output written to: {filepath}")
        
        return output
    
    def output_format(self, format_type: str, filepath: str = None) -> str:
        """Output in specified format."""
        formatter = FormattersFactory().get_formatter(format_type.lower())
        
        # Format each entry
        output_lines = []
        for entry in self.entries:
            entry_dict = {
                'author': entry.authors,
                'title': entry.title,
                'journal': entry.journal,
                'year': entry.year,
                'volume': entry.volume,
                'page': entry.pages,
                'entry_id': entry.entry_id
            }
            formatted = formatter.format(entry_dict)
            output_lines.append(formatted)
        
        output = '\n'.join(output_lines)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✓ {format_type.upper()} output written to: {filepath}")
        
        return output
    
    def generate_quality_report(self, export_path: str = None):
        """Generate quality report."""
        print("\n" + "="*60)
        print("QUALITY REPORT")
        print("="*60)
        
        for entry in self.entries:
            entry_dict = {
                'entry_id': entry.entry_id,
                'author': entry.authors,
                'title': entry.title,
                'journal': entry.journal,
                'year': entry.year,
                'volume': entry.volume,
                'pages': entry.pages
            }
            report = self.qa.get_quality_report(entry_dict)
            print(f"\n{entry.entry_id}:")
            print(f"  Overall Score: {report['overall_score']*100:.1f}%")
            print(f"  Completeness: {report['completeness']:.1f}%")
            if report['issues']:
                print(f"  Issues: {', '.join(report['issues'])}")
            if report['recommendations']:
                print(f"  Recommendations: {', '.join(report['recommendations'])}")
        
        if export_path:
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write("BIBLIOGRAPHY QUALITY REPORT\n")
                f.write("="*60 + "\n\n")
                for entry in self.entries:
                    entry_dict = {
                        'entry_id': entry.entry_id,
                        'author': entry.authors,
                        'title': entry.title,
                        'journal': entry.journal,
                        'year': entry.year,
                        'volume': entry.volume,
                        'pages': entry.pages
                    }
                    report = self.qa.get_quality_report(entry_dict)
                    f.write(f"\n{entry.entry_id}:\n")
                    f.write(f"  Overall Score: {report['overall_score']*100:.1f}%\n")
                    f.write(f"  Completeness: {report['completeness']:.1f}%\n")
                    if report['issues']:
                        f.write(f"  Issues: {', '.join(report['issues'])}\n")
                    if report['recommendations']:
                        f.write(f"  Recommendations: {', '.join(report['recommendations'])}\n")
            print(f"✓ Report written to: {export_path}")
    
    def close(self):
        """Close resources."""
        if self.db:
            self.db.close()


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Enhanced Bibliography Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert to BibTeX
  python -m src.enhanced_main input.txt output.bib
  
  # Convert to IEEE format
  python -m src.enhanced_main input.txt output.txt --format ieee
  
  # With French language
  python -m src.enhanced_main input.txt output.bib --language fr
  
  # With quality report
  python -m src.enhanced_main input.txt output.bib --quality
        """
    )
    
    parser.add_argument('input_file', help='Input file with references')
    parser.add_argument('output_file', nargs='?', help='Output file (optional)')
    parser.add_argument('-f', '--format', 
                       choices=['bibtex', 'ieee', 'apa', 'chicago', 'mla'],
                       default='bibtex',
                       help='Output format (default: bibtex)')
    parser.add_argument('-l', '--language',
                       choices=['en', 'fr', 'es', 'de', 'zh'],
                       default='en',
                       help='Language (default: en)')
    parser.add_argument('-q', '--quality',
                       action='store_true',
                       help='Generate quality report')
    
    return parser


def main():
    """Main function."""
    parser_arg = create_parser()
    args = parser_arg.parse_args()
    
    # Set language
    lang_map = {
        'en': Language.EN,
        'fr': Language.FR,
        'es': Language.ES,
        'de': Language.DE,
        'zh': Language.ZH
    }
    language = lang_map.get(args.language, Language.EN)
    
    # Create generator
    generator = EnhancedBibliographyGenerator(language=language)
    
    # Process input file
    if args.input_file:
        generator.process_file(args.input_file)
        
        # Output in specified format
        if args.output_file:
            if args.format == 'bibtex':
                generator.output_bibtex(args.output_file)
            else:
                generator.output_format(args.format, args.output_file)
        
        # Generate report if requested
        if args.quality:
            generator.generate_quality_report()
    
    generator.close()


if __name__ == "__main__":
    main()
