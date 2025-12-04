"""
Optimized ML field extraction with fast scoring.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ExtractionConfidence:
    """Confidence scores for extracted fields."""
    author: float = 0.0
    title: float = 0.0
    journal: float = 0.0
    year: float = 0.0
    volume: float = 0.0
    pages: float = 0.0
    
    def get_average(self) -> float:
        """Get average confidence."""
        scores = [self.author, self.title, self.journal, self.year, self.volume, self.pages]
        scores = [s for s in scores if s > 0]
        return sum(scores) / len(scores) if scores else 0.0


class MLFieldExtractor:
    """Optimized ML field extractor with caching."""
    
    # Pre-computed confidence weights
    _WEIGHTS = {
        'author': {'patterns': 1.0, 'capital_words': 0.3, 'commas': 0.2},
        'title': {'length': 0.5, 'capitals': 0.3, 'quotes': 0.4},
        'journal': {'capitals': 0.6, 'keywords': 0.5},
        'year': {'pattern': 1.0},
        'volume': {'format': 0.9},
        'pages': {'pattern': 0.8},
    }
    
    def __init__(self):
        self._cache = {}
    
    def extract_with_confidence(self, entry: dict) -> ExtractionConfidence:
        """Extract fields with confidence scores."""
        cache_key = hash(str(entry))
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        confidence = ExtractionConfidence()
        
        # Score author
        author = entry.get('author', '')
        confidence.author = self._score_author(author)
        
        # Score title
        title = entry.get('title', '')
        confidence.title = self._score_title(title)
        
        # Score journal
        journal = entry.get('journal', '')
        confidence.journal = self._score_journal(journal)
        
        # Score year
        year = entry.get('year', '')
        confidence.year = 1.0 if year and len(year) == 4 and year.isdigit() else 0.0
        
        # Score volume
        volume = entry.get('volume', '')
        confidence.volume = 1.0 if volume and volume.isdigit() else 0.0
        
        # Score pages
        pages = entry.get('pages', '')
        confidence.pages = self._score_pages(pages)
        
        self._cache[cache_key] = confidence
        return confidence
    
    def _score_author(self, author: str) -> float:
        """Score author field."""
        if not author:
            return 0.0
        
        score = 0.0
        
        # Check for commas (indicates multiple authors)
        if ',' in author:
            score += 0.2
        
        # Check for capital letters
        capital_count = sum(1 for c in author if c.isupper())
        if capital_count >= 2:
            score += 0.3
        
        # Check for "and" or "&"
        if ' and ' in author or ' & ' in author:
            score += 0.2
        
        # Check for "et al."
        if 'et al' in author.lower():
            score += 0.3
        
        return min(score, 1.0)
    
    def _score_title(self, title: str) -> float:
        """Score title field."""
        if not title or len(title) < 5:
            return 0.0
        
        score = 0.0
        
        # Check length
        if len(title) > 10:
            score += 0.3
        
        # Check capital letters
        capital_count = sum(1 for c in title if c.isupper())
        if capital_count >= 3:
            score += 0.3
        
        # Check for quotes
        if '"' in title or "'" in title:
            score += 0.2
        
        return min(score, 1.0)
    
    def _score_journal(self, journal: str) -> float:
        """Score journal field."""
        if not journal:
            return 0.0
        
        score = 0.0
        
        # Check capital letters
        capital_count = sum(1 for c in journal if c.isupper())
        if capital_count >= 2:
            score += 0.4
        
        # Check for journal keywords
        journal_lower = journal.lower()
        keywords = ['journal', 'review', 'transactions', 'proceedings', 'communications', 'letters']
        if any(kw in journal_lower for kw in keywords):
            score += 0.4
        
        return min(score, 1.0)
    
    def _score_pages(self, pages: str) -> float:
        """Score pages field."""
        if not pages:
            return 0.0
        
        # Check for page range format (e.g., "123-456")
        if '-' in pages and any(c.isdigit() for c in pages):
            return 1.0
        
        # Check if all digits
        if pages.isdigit():
            return 0.8
        
        return 0.0
    
    def clear_cache(self):
        """Clear extraction cache."""
        self._cache.clear()


class QualityAssurance:
    """Quality assurance for bibliography entries."""
    
    def __init__(self):
        self.ml_extractor = MLFieldExtractor()
    
    def get_quality_report(self, entry: dict) -> Dict:
        """Generate quality report for an entry."""
        confidence = self.ml_extractor.extract_with_confidence(entry)
        
        report = {
            'entry_id': entry.get('entry_id', 'unknown'),
            'overall_score': confidence.get_average(),
            'field_scores': {
                'author': confidence.author,
                'title': confidence.title,
                'journal': confidence.journal,
                'year': confidence.year,
                'volume': confidence.volume,
                'pages': confidence.pages,
            },
            'completeness': self._calculate_completeness(entry),
            'issues': self._identify_issues(entry),
            'recommendations': self._generate_recommendations(confidence, entry),
        }
        
        return report
    
    def _calculate_completeness(self, entry: dict) -> float:
        """Calculate entry completeness percentage."""
        required_fields = ['author', 'title', 'year']
        optional_fields = ['journal', 'volume', 'pages']
        
        present_required = sum(1 for f in required_fields if entry.get(f))
        present_optional = sum(1 for f in optional_fields if entry.get(f))
        
        required_score = present_required / len(required_fields) * 0.7
        optional_score = present_optional / len(optional_fields) * 0.3
        
        return (required_score + optional_score) * 100
    
    def _identify_issues(self, entry: dict) -> list:
        """Identify issues with entry."""
        issues = []
        
        if not entry.get('author'):
            issues.append("Missing author")
        
        if not entry.get('title') or len(entry.get('title', '')) < 5:
            issues.append("Missing or invalid title")
        
        if not entry.get('year'):
            issues.append("Missing year")
        
        year = entry.get('year', '')
        if year and (not year.isdigit() or len(year) != 4):
            issues.append("Invalid year format")
        
        return issues
    
    def _generate_recommendations(self, confidence: ExtractionConfidence, entry: dict) -> list:
        """Generate recommendations for improvement."""
        recommendations = []
        
        if confidence.author < 0.5:
            recommendations.append("Improve author field formatting")
        
        if confidence.title < 0.5:
            recommendations.append("Ensure title is properly capitalized and quoted")
        
        if confidence.journal < 0.5 and entry.get('journal'):
            recommendations.append("Verify journal name format")
        
        return recommendations
