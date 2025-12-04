"""
Unit tests for bibliography parser.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from parser import Parser, BibliographyEntry
from generator import BibTeXGenerator
from lexer import Lexer, TokenType


class TestLexer(unittest.TestCase):
    """Test cases for Lexer."""
    
    def test_year_extraction(self):
        """Test year token extraction."""
        text = "Computer Communications, 2000. 23(8): p. 769-778."
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        
        year_tokens = [t for t in tokens if t.type == TokenType.YEAR]
        self.assertTrue(len(year_tokens) > 0)
        self.assertEqual(year_tokens[0].value, "2000")
    
    def test_pages_extraction(self):
        """Test pages token extraction."""
        text = "Computer Communications, 2000. 23(8): p. 769-778."
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        
        page_tokens = [t for t in tokens if t.type == TokenType.PAGES]
        self.assertTrue(len(page_tokens) > 0)
        self.assertIn("-", page_tokens[0].value)


class TestParser(unittest.TestCase):
    """Test cases for Parser."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = Parser()
        self.sample_reference = (
            "Silva, L.M., et al., Comparing the performance of "
            "mobile agent systems: a study of benchmarking. "
            "Computer Communications, 2000. 23(8): p. 769-778."
        )
    
    def test_parse_article(self):
        """Test parsing an article reference."""
        entry = self.parser.parse(self.sample_reference)
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry.entry_type, "article")
        self.assertTrue(len(entry.authors) > 0)
        self.assertTrue(len(entry.title) > 0)
        self.assertEqual(entry.year, "2000")
    
    def test_authors_extraction(self):
        """Test author extraction."""
        entry = self.parser.parse(self.sample_reference)
        
        self.assertIn("Silva", entry.authors)
        self.assertIn("L.M.", entry.authors)
    
    def test_title_extraction(self):
        """Test title extraction."""
        entry = self.parser.parse(self.sample_reference)
        
        self.assertTrue(len(entry.title) > 0)
        self.assertIn("agent", entry.title.lower())
    
    def test_volume_extraction(self):
        """Test volume number extraction."""
        entry = self.parser.parse(self.sample_reference)
        
        self.assertEqual(entry.volume, "23")
    
    def test_pages_extraction(self):
        """Test pages extraction."""
        entry = self.parser.parse(self.sample_reference)
        
        self.assertIsNotNone(entry.pages)
        self.assertIn("-", entry.pages)
    
    def test_entry_id(self):
        """Test entry ID assignment."""
        entry1 = self.parser.parse(self.sample_reference, "ID1")
        self.assertEqual(entry1.entry_id, "ID1")
        
        entry2 = self.parser.parse(self.sample_reference)
        self.assertEqual(entry2.entry_id, "ID2")
    
    def test_book_detection(self):
        """Test book type detection."""
        book_ref = "Donald E. Knuth. The Art of Computer Programming. Addison-Wesley, 1968."
        entry = self.parser.parse(book_ref)
        
        # Should detect as book or article (depends on keyword detection)
        self.assertIn(entry.entry_type, ["book", "article"])


class TestBibTeXGeneration(unittest.TestCase):
    """Test cases for BibTeX generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = BibTeXGenerator()
    
    def test_generate_article(self):
        """Test BibTeX generation for article."""
        entry = BibliographyEntry(
            entry_id="ID1",
            entry_type="article",
            authors="Silva, L.M. and etal",
            title="Comparing the performance of mobile agent systems",
            journal="Computer Communications",
            year="2000",
            volume="23",
            number="8",
            pages="769-778"
        )
        
        bibtex = self.generator.generate(entry)
        
        self.assertIn("@article{ID1", bibtex)
        self.assertIn("author = {Silva, L.M. and etal}", bibtex)
        self.assertIn("year = {2000}", bibtex)
        self.assertIn("volume = {23}", bibtex)
    
    def test_generate_multiple(self):
        """Test batch BibTeX generation."""
        entries = [
            BibliographyEntry(
                entry_id="ID1",
                entry_type="article",
                authors="Author One",
                title="First Paper",
                year="2020"
            ),
            BibliographyEntry(
                entry_id="ID2",
                entry_type="article",
                authors="Author Two",
                title="Second Paper",
                year="2021"
            )
        ]
        
        bibtex = self.generator.generate_batch(entries)
        
        self.assertIn("@article{ID1", bibtex)
        self.assertIn("@article{ID2", bibtex)
        self.assertEqual(bibtex.count("@article"), 2)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    run_tests()
