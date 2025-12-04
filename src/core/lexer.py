"""
Optimized lexer with pre-compiled regex patterns.
Single-pass tokenization for maximum performance.
"""

import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    """Token types for bibliographic references."""
    AUTHOR = "AUTHOR"
    YEAR = "YEAR"
    TITLE = "TITLE"
    JOURNAL = "JOURNAL"
    VOLUME = "VOLUME"
    NUMBER = "NUMBER"
    PAGES = "PAGES"
    PUBLISHER = "PUBLISHER"
    SCHOOL = "SCHOOL"
    UNKNOWN = "UNKNOWN"


@dataclass
class Token:
    """Represents a lexical token."""
    type: TokenType
    value: str
    position: int


class OptimizedLexer:
    """Optimized lexical analyzer with pre-compiled patterns."""
    
    # Pre-compiled patterns for maximum performance
    _YEAR_PATTERN = re.compile(r'\b(19|20)\d{2}\b')
    _VOLUME_PATTERN = re.compile(r'(?:volume|vol\.?|v\.)\s*(?:=|:|\.?\s)?(\d+)', re.IGNORECASE)
    _NUMBER_PATTERN = re.compile(r'(?:no(?:\.)?|number|n\.)\s*(?:=|:|\.?\s)?\(?(\d+)\)?', re.IGNORECASE)
    _PAGES_PATTERN = re.compile(r'(?:pp?\.?|pages?|p\.)\s*(?:=|:|\.?\s)?(\d+)\s*[-–—]\s*(\d+)', re.IGNORECASE)
    _SENTENCE_SPLIT = re.compile(r'(?<=[.;,])\s+')
    
    def __init__(self, text: str):
        self.text = text
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """Fast single-pass tokenization."""
        self.tokens.clear()
        
        # Fast year extraction (single pass)
        for match in self._YEAR_PATTERN.finditer(self.text):
            self.tokens.append(Token(TokenType.YEAR, match.group(), match.start()))
        
        # Fast volume extraction
        for match in self._VOLUME_PATTERN.finditer(self.text):
            self.tokens.append(Token(TokenType.VOLUME, match.group(1), match.start()))
        
        # Fast number extraction
        for match in self._NUMBER_PATTERN.finditer(self.text):
            self.tokens.append(Token(TokenType.NUMBER, match.group(1), match.start()))
        
        # Fast pages extraction with fallback
        for match in self._PAGES_PATTERN.finditer(self.text):
            pages = f"{match.group(1)}-{match.group(2)}"
            self.tokens.append(Token(TokenType.PAGES, pages, match.start()))
        
        # If no pages found, try fallback pattern
        if not any(t.type == TokenType.PAGES for t in self.tokens):
            fallback = re.compile(r'(\d{2,})\s*[-–—]\s*(\d{2,})')
            for match in fallback.finditer(self.text):
                pages = f"{match.group(1)}-{match.group(2)}"
                self.tokens.append(Token(TokenType.PAGES, pages, match.start()))
        
        return sorted(self.tokens, key=lambda t: t.position)
    
    def get_tokens_by_type(self, token_type: TokenType) -> List[Token]:
        """Fast token type lookup."""
        return [t for t in self.tokens if t.type == token_type]
