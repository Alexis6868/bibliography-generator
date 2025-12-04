"""
Tests for new features (formatters, ML extraction, database, i18n, UI).
"""

import sys
import os
import unittest
import tempfile

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from parser import Parser, BibliographyEntry
from formatters import IEEEFormatter, APAFormatter, ChicagoFormatter, MLAFormatter, FormattersFactory, CitationFormat
from ml_extractor import MLFieldExtractor, QualityAssurance
from database import BibliographyDatabase
from i18n import I18nManager, Language, translate
from ui import InteractiveCorrectionUI, BatchCorrectionUI


class TestFormatters(unittest.TestCase):
    """Test citation formatters."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.entry = BibliographyEntry(
            entry_id="TEST1",
            entry_type="article",
            authors="Silva, L.M. and etal",
            title="Comparing the performance of mobile agent systems",
            journal="Computer Communications",
            year="2000",
            volume="23",
            number="8",
            pages="769-778"
        )
    
    def test_ieee_formatter(self):
        """Test IEEE format."""
        formatter = IEEEFormatter()
        output = formatter.format(self.entry)
        
        self.assertIn("Silva", output)
        self.assertIn("2000", output)
        self.assertIn("Computer Communications", output)
    
    def test_apa_formatter(self):
        """Test APA format."""
        formatter = APAFormatter()
        output = formatter.format(self.entry)
        
        self.assertIn("Silva", output)
        self.assertIn("2000", output)
    
    def test_chicago_formatter(self):
        """Test Chicago format."""
        formatter = ChicagoFormatter()
        output = formatter.format(self.entry)
        
        self.assertIn("Silva", output)
        self.assertIn("2000", output)
    
    def test_mla_formatter(self):
        """Test MLA format."""
        formatter = MLAFormatter()
        output = formatter.format(self.entry)
        
        self.assertIn("Silva", output)
        self.assertIn("2000", output)
    
    def test_factory(self):
        """Test formatter factory."""
        formatter = FormattersFactory.get_formatter(CitationFormat.IEEE)
        self.assertIsInstance(formatter, IEEEFormatter)


class TestMLExtractor(unittest.TestCase):
    """Test ML field extractor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.extractor = MLFieldExtractor()
        self.entry = BibliographyEntry(
            entry_id="TEST1",
            entry_type="article",
            authors="Silva, L.M. and etal",
            title="Comparing the performance of mobile agent systems",
            journal="Computer Communications",
            year="2000",
            volume="23",
            number="8",
            pages="769-778"
        )
        self.text = "Silva, L.M., et al., Comparing the performance. Computer Communications, 2000."
    
    def test_confidence_scoring(self):
        """Test confidence scoring."""
        confidence = self.extractor.evaluate_extraction(self.entry, self.text)
        
        self.assertGreater(confidence.year_score, 0.5)
        self.assertGreater(confidence.overall_score, 0.0)
    
    def test_quality_validation(self):
        """Test entry validation."""
        is_valid, issues = QualityAssurance.validate_entry(self.entry)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
    
    def test_quality_validation_missing_fields(self):
        """Test validation with missing fields."""
        incomplete_entry = BibliographyEntry(
            entry_id="TEST2",
            entry_type="article",
            authors="",
            title=""
        )
        
        is_valid, issues = QualityAssurance.validate_entry(incomplete_entry)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)
    
    def test_completeness_score(self):
        """Test completeness scoring."""
        score = QualityAssurance.calculate_completeness_score(self.entry)
        
        self.assertGreater(score, 0.5)


class TestDatabase(unittest.TestCase):
    """Test database functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.db = BibliographyDatabase(":memory:")
        self.entry = BibliographyEntry(
            entry_id="TEST1",
            entry_type="article",
            authors="Silva, L.M.",
            title="Test Article",
            year="2000"
        )
    
    def test_add_entry(self):
        """Test adding entry."""
        result = self.db.add_entry(self.entry)
        self.assertTrue(result)
    
    def test_get_entry(self):
        """Test retrieving entry."""
        self.db.add_entry(self.entry)
        retrieved = self.db.get_entry("TEST1")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.entry_id, "TEST1")
    
    def test_search_entries(self):
        """Test searching entries."""
        self.db.add_entry(self.entry)
        results = self.db.search_entries("Silva")
        
        self.assertEqual(len(results), 1)
    
    def test_add_tag(self):
        """Test adding tags."""
        self.db.add_entry(self.entry)
        result = self.db.add_tag("TEST1", "important")
        
        self.assertTrue(result)
        tags = self.db.get_tags("TEST1")
        self.assertIn("important", tags)
    
    def test_add_note(self):
        """Test adding notes."""
        self.db.add_entry(self.entry)
        result = self.db.add_note("TEST1", "Review this paper")
        
        self.assertTrue(result)
        notes = self.db.get_notes("TEST1")
        self.assertIn("Review this paper", notes)
    
    def tearDown(self):
        """Clean up."""
        self.db.close()


class TestI18n(unittest.TestCase):
    """Test internationalization."""
    
    def test_english_translation(self):
        """Test English translation."""
        i18n = I18nManager(Language.ENGLISH)
        result = i18n.translate('author')
        
        self.assertEqual(result, 'Author')
    
    def test_french_translation(self):
        """Test French translation."""
        i18n = I18nManager(Language.FRENCH)
        result = i18n.translate('author')
        
        self.assertEqual(result, 'Auteur')
    
    def test_spanish_translation(self):
        """Test Spanish translation."""
        i18n = I18nManager(Language.SPANISH)
        result = i18n.translate('author')
        
        self.assertEqual(result, 'Autor')
    
    def test_language_switch(self):
        """Test switching language."""
        i18n = I18nManager(Language.ENGLISH)
        self.assertEqual(i18n.translate('author'), 'Author')
        
        i18n.set_language(Language.FRENCH)
        self.assertEqual(i18n.translate('author'), 'Auteur')
    
    def test_missing_translation(self):
        """Test fallback for missing translations."""
        i18n = I18nManager(Language.ENGLISH)
        result = i18n.translate('nonexistent_key', 'default_value')
        
        self.assertEqual(result, 'default_value')


class TestBatchCorrectionUI(unittest.TestCase):
    """Test batch correction UI."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ui = BatchCorrectionUI()
        self.entries = [
            BibliographyEntry(
                entry_id="TEST1",
                entry_type="article",
                authors="Silva, L.M.",
                title="Article 1",
                year="2000"
            ),
            BibliographyEntry(
                entry_id="TEST2",
                entry_type="book",
                authors="Author Name",
                title="Book Title",
                year="2020"
            )
        ]
    
    def test_report_generation(self):
        """Test report generation."""
        report = self.ui.generate_report(self.entries)
        
        self.assertIn("BIBLIOGRAPHY QUALITY REPORT", report)
        self.assertIn("Total entries: 2", report)
    
    def test_report_contains_statistics(self):
        """Test report contains statistics."""
        report = self.ui.generate_report(self.entries)
        
        self.assertIn("Average completeness", report)
        self.assertIn("Field Presence", report)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    run_tests()
