"""
Optimized parser with caching and fast extraction.
"""

import re
from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class CachedEntry:
    """Entry with cached extraction results."""
    entry_id: str
    entry_type: str
    authors: str = ""
    title: str = ""
    journal: Optional[str] = None
    year: Optional[str] = None
    volume: Optional[str] = None
    number: Optional[str] = None
    pages: Optional[str] = None
    publisher: Optional[str] = None
    school: Optional[str] = None


class OptimizedParser:
    """Fast parser with caching and optimized extraction."""
    
    # Pre-compiled patterns for fast matching
    _AUTHOR_PATTERN = re.compile(
        r'^([A-Za-z\-]+(?:\s+[A-Za-z\-]+)*(?:,\s*[A-Z]\.(?:[A-Z]\.)?)*(?:\s*,\s*(?:et\s+)?al\.)?)',
        re.MULTILINE
    )
    _JOURNAL_PATTERNS = [
        re.compile(r'\b([A-Z][A-Za-z\s&]*(?:Journal|Transactions|Letters|Review|Proceedings|Communications))\b'),
        re.compile(r'\b([A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]*)*)\s+(?:Communications|Journal|Review|Proceedings)\b')
    ]
    
    def __init__(self):
        self.entry_counter = 0
        self._cache: Dict[str, CachedEntry] = {}
    
    def parse(self, text: str, entry_id: Optional[str] = None, use_cache: bool = True) -> CachedEntry:
        """Parse reference with optional caching."""
        # Check cache
        cache_key = hash(text) if use_cache else None
        if cache_key and cache_key in self._cache:
            return self._cache[cache_key]
        
        self.entry_counter += 1
        if not entry_id:
            entry_id = f"ID{self.entry_counter}"
        
        # Fast extraction (all in parallel)
        entry = CachedEntry(
            entry_id=entry_id,
            entry_type=self._extract_entry_type_fast(text),
            authors=self._extract_authors_fast(text),
            title=self._extract_title_fast(text),
            year=self._extract_year_fast(text),
            journal=self._extract_journal_fast(text),
            volume=self._extract_volume_fast(text),
            number=self._extract_number_fast(text),
            pages=self._extract_pages_fast(text)
        )
        
        if use_cache and cache_key:
            self._cache[cache_key] = entry
        
        return entry
    
    def _extract_authors_fast(self, text: str) -> str:
        """Fast author extraction."""
        match = self._AUTHOR_PATTERN.match(text)
        if match:
            authors = match.group(1).strip()
            authors = re.sub(r',\s*et\s+al\.', ' and etal', authors)
            return re.sub(r'\s+', ' ', authors)
        return ""
    
    def _extract_title_fast(self, text: str) -> str:
        """Fast title extraction."""
        author_end = 0
        if "et al." in text:
            author_end = text.find("et al.") + len("et al.")
        else:
            first_period = text.find('.')
            if first_period > 0:
                author_part = text[:first_period]
                last_comma = author_part.rfind(',')
                if last_comma > 0:
                    author_end = last_comma + 1
        
        remaining = text[author_end:].lstrip(", ")
        title_match = re.match(r'^([A-Z][^.]*?)(?:\s*[.,]\s*(?:[A-Z][a-z]+(?:\s+[A-Z]|,|\d)|$))', remaining)
        
        if title_match:
            title = title_match.group(1).strip()
        else:
            first_sentence = remaining.split('.')[0] if '.' in remaining else remaining
            title = first_sentence.strip()
        
        title = re.sub(r'\s+', ' ', title)
        return title if len(title) > 5 else ""
    
    def _extract_year_fast(self, text: str) -> Optional[str]:
        """Fast year extraction."""
        match = re.search(r'\b(19|20)\d{2}\b', text)
        return match.group() if match else None
    
    def _extract_journal_fast(self, text: str) -> Optional[str]:
        """Fast journal extraction with multiple patterns."""
        for pattern in self._JOURNAL_PATTERNS:
            match = pattern.search(text)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_volume_fast(self, text: str) -> Optional[str]:
        """Fast volume extraction."""
        match = re.search(r'(?:volume|vol\.?|v\.)\s*(?:=|:|\.?\s)?(\d+)', text, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _extract_number_fast(self, text: str) -> Optional[str]:
        """Fast number extraction."""
        match = re.search(r'\((\d+)\)', text)
        return match.group(1) if match else None
    
    def _extract_pages_fast(self, text: str) -> Optional[str]:
        """Fast pages extraction."""
        match = re.search(r'(\d{2,})\s*[-–—]\s*(\d{2,})', text)
        if match:
            return f"{match.group(1)}-{match.group(2)}"
        return None
    
    def _extract_entry_type_fast(self, text: str) -> str:
        """Fast entry type detection."""
        text_lower = text.lower()
        
        # Quick checks in order of likelihood
        if 'phd thesis' in text_lower or 'dissertation' in text_lower:
            return 'phdthesis'
        elif 'master' in text_lower:
            return 'mastersthesis'
        elif 'proceedings' in text_lower or 'conference' in text_lower:
            return 'inproceedings'
        elif 'publisher' in text_lower or 'press' in text_lower:
            return 'book'
        
        return 'article'  # Default
    
    def clear_cache(self):
        """Clear parser cache."""
        self._cache.clear()
