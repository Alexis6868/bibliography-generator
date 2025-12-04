"""
Bibliography Generator - A transpiler for converting text references to BibTeX format.

Main modules:
- src.core: Core transpiler (lexer, parser, generator)
- src.features: Feature implementations (formatters)
- src.utils: Utility modules (ml_extractor, database, i18n)
"""

__version__ = "2.0.0"
__author__ = "Project Team - SY48"

# Import optimized modules from core
from src.core.lexer import OptimizedLexer
from src.core.parser import OptimizedParser
from src.core.generator import OptimizedBibTeXGenerator

# For backward compatibility, create aliases
Lexer = OptimizedLexer
Parser = OptimizedParser
BibTeXGenerator = OptimizedBibTeXGenerator

__all__ = [
    'Lexer',
    'Parser',
    'BibTeXGenerator',
    'OptimizedLexer',
    'OptimizedParser',
    'OptimizedBibTeXGenerator',
]
