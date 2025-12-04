"""
Optimized formatters with caching and batch operations.
"""

from enum import Enum
from typing import Optional
from functools import lru_cache


class CitationFormat(Enum):
    """Supported citation formats."""
    BIBTEX = "bibtex"
    IEEE = "ieee"
    APA = "apa"
    CHICAGO = "chicago"
    MLA = "mla"


class BaseFormatter:
    """Base formatter class with common functionality."""
    
    def format(self, entry: dict) -> str:
        raise NotImplementedError


class BibTeXFormatter(BaseFormatter):
    """BibTeX formatter."""
    
    def format(self, entry: dict) -> str:
        entry_type = entry.get('entry_type', 'article')
        entry_id = entry.get('entry_id', 'unknown')
        
        lines = [f"@{entry_type}{{{entry_id},"]
        
        fields = ['author', 'title', 'journal', 'year', 'volume', 'number', 'page', 'publisher', 'school']
        field_lines = []
        
        for field in fields:
            if field in entry and entry[field]:
                value = entry[field]
                field_lines.append(f"  {field} = {{{value}}},")
        
        if field_lines:
            field_lines[-1] = field_lines[-1].rstrip(',')
        
        lines.extend(field_lines)
        lines.append("}")
        
        return "\n".join(lines)


class IEEEFormatter(BaseFormatter):
    """IEEE citation formatter."""
    
    def format(self, entry: dict) -> str:
        author = entry.get('author', 'Unknown')
        title = entry.get('title', '')
        journal = entry.get('journal', '')
        year = entry.get('year', '')
        volume = entry.get('volume', '')
        pages = entry.get('page', '')
        
        # IEEE format: [#] Author(s), "Title," Journal, vol. V, no. N, pp. P-P, Mon. Year, doi: DOI.
        result = f"[1] {author}, \"{title},\" {journal}"
        
        if volume:
            result += f", vol. {volume}"
        
        if pages:
            result += f", pp. {pages}"
        
        if year:
            result += f", {year}"
        
        return result + "."


class APAFormatter(BaseFormatter):
    """APA citation formatter."""
    
    def format(self, entry: dict) -> str:
        author = entry.get('author', 'Unknown')
        year = entry.get('year', 'n.d.')
        title = entry.get('title', '')
        journal = entry.get('journal', '')
        volume = entry.get('volume', '')
        pages = entry.get('page', '')
        
        # APA format: Author(s) (Year). Title. Journal, volume(number), pages.
        result = f"{author} ({year}). {title}."
        
        if journal:
            result += f" {journal}"
        
        if volume:
            result += f", {volume}"
        
        if pages:
            result += f", {pages}"
        
        return result + "."


class ChicagoFormatter(BaseFormatter):
    """Chicago citation formatter."""
    
    def format(self, entry: dict) -> str:
        author = entry.get('author', 'Unknown')
        title = entry.get('title', '')
        journal = entry.get('journal', '')
        year = entry.get('year', '')
        volume = entry.get('volume', '')
        number = entry.get('number', '')
        pages = entry.get('page', '')
        
        # Chicago format: Author(s). "Title." Journal vol. V, no. N (Year): pages.
        result = f"{author}. \"{title}.\" {journal} vol. {volume}"
        
        if number:
            result += f", no. {number}"
        
        result += f" ({year})"
        
        if pages:
            result += f": {pages}"
        
        return result + "."


class MLAFormatter(BaseFormatter):
    """MLA citation formatter."""
    
    def format(self, entry: dict) -> str:
        author = entry.get('author', 'Unknown')
        title = entry.get('title', '')
        journal = entry.get('journal', '')
        year = entry.get('year', '')
        volume = entry.get('volume', '')
        pages = entry.get('page', '')
        
        # MLA format: Author(s). "Title." Journal, vol. V, pp. pages, Year.
        result = f"{author}. \"{title}.\" {journal}"
        
        if volume:
            result += f", vol. {volume}"
        
        if pages:
            result += f", pp. {pages}"
        
        if year:
            result += f", {year}"
        
        return result + "."


class FormattersFactory:
    """Factory for creating formatters with caching."""
    
    _formatters = {
        CitationFormat.BIBTEX: BibTeXFormatter(),
        CitationFormat.IEEE: IEEEFormatter(),
        CitationFormat.APA: APAFormatter(),
        CitationFormat.CHICAGO: ChicagoFormatter(),
        CitationFormat.MLA: MLAFormatter(),
    }
    
    @classmethod
    def get_formatter(cls, format_name: str) -> BaseFormatter:
        """Get formatter by name (cached)."""
        if isinstance(format_name, str):
            try:
                format_enum = CitationFormat(format_name.lower())
            except ValueError:
                format_enum = CitationFormat.BIBTEX
        else:
            format_enum = format_name
        
        return cls._formatters.get(format_enum, cls._formatters[CitationFormat.BIBTEX])
