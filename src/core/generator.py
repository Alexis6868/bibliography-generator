"""
Optimized BibTeX generator with batch processing.
"""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class BibEntry:
    """BibTeX entry."""
    entry_id: str
    entry_type: str
    authors: str
    title: str
    journal: Optional[str] = None
    year: Optional[str] = None
    volume: Optional[str] = None
    number: Optional[str] = None
    pages: Optional[str] = None
    publisher: Optional[str] = None
    school: Optional[str] = None


class OptimizedBibTeXGenerator:
    """Optimized BibTeX generator with batch support."""
    
    # Field order template
    FIELD_ORDER = ['author', 'title', 'journal', 'year', 'volume', 'number', 'page', 'publisher', 'school']
    
    def __init__(self, indent: str = "  "):
        self.indent = indent
    
    def generate(self, entry: BibEntry) -> str:
        """Generate single BibTeX entry."""
        lines = [f"@{entry.entry_type}{{{entry.entry_id},"]
        
        # Build field list
        fields = [
            ('author', entry.authors),
            ('title', entry.title),
            ('journal', entry.journal),
            ('year', entry.year),
            ('volume', entry.volume),
            ('number', entry.number),
            ('page', entry.pages),
            ('publisher', entry.publisher),
            ('school', entry.school),
        ]
        
        # Add fields
        field_lines = []
        for field_name, value in fields:
            if value:
                field_lines.append(f"{self.indent}{field_name} = {{{value}}},")
        
        # Remove trailing comma from last field
        if field_lines:
            field_lines[-1] = field_lines[-1].rstrip(',')
        
        lines.extend(field_lines)
        lines.append("}")
        
        return "\n".join(lines)
    
    def generate_batch(self, entries: List[BibEntry]) -> str:
        """Generate multiple entries efficiently."""
        return "\n\n".join(self.generate(entry) for entry in entries)
    
    def generate_file(self, entries: List[BibEntry], filepath: str) -> None:
        """Generate and write to file in one operation."""
        content = self.generate_batch(entries)
        with open(filepath, 'w', encoding='utf-8', buffering=1024*64) as f:
            f.write(content)
