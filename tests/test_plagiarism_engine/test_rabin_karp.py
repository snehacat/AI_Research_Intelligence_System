"""
Tests for Rabin-Karp plagiarism detection engine.
"""
import pytest
from plagiarism_engine.rabin_karp import RabinKarpPlagiarism, RabinKarpResult, MatchResult
from utils.exceptions import InsufficientDataError, PlagiarismDetectionError


class TestRabinKarpPlagiarism:
    """Test RabinKarpPlagiarism class"""
    
    def test_initialization_default(self):
        """Test default initialization"""
        rk = RabinKarpPlagiarism()
        assert rk.window_size == 5
        assert rk.min_window_size == 3
        assert rk.max_window_size == 15
    
    def test_initialization_custom_window(self):
        """Test initialization with custom window size"""
        rk = RabinKarpPlagiarism(window_size=7)
        assert rk.window_size == 7
    
    def test_initialization_invalid_window(self):
        """Test initialization with invalid window size"""
        with pytest.raises(ValueError):
            RabinKarpPlagiarism(window_size=20, max_window_size=15)
    
    def test_generate_fingerprints_basic(self, sample_document_words):
        """Test fingerprint generation"""
        rk = RabinKarpPlagiarism(window_size=3)
        fingerprints = rk.generate_fingerprints(sample_document_words)
        assert len(fingerprints) > 0
        assert all(isinstance(k, int) for k in fingerprints.keys())
    
    def test_generate_fingerprints_short_text(self):
        """Test fingerprint generation with text shorter than window"""
        rk = RabinKarpPlagiarism(window_size=5)
        words = ["one", "two", "three"]
        fingerprints = rk.generate_fingerprints(words)
        assert len(fingerprints) == 0
    
    def test_generate_fingerprints_empty(self):
        """Test fingerprint generation with empty input"""
        rk = RabinKarpPlagiarism()
        fingerprints = rk.generate_fingerprints([])
        assert len(fingerprints) == 0
    
    def test_calculate_similarity_exact_match(self):
        """Test similarity calculation with exact match"""
        rk = RabinKarpPlagiarism(window_size=3)
        doc_words = ["the", "quick", "brown", "fox", "jumps"]
        ref_words = ["the", "quick", "brown", "fox", "jumps"]
        
        result = rk.calculate_similarity(doc_words, [ref_words])
        assert isinstance(result, RabinKarpResult)
        assert result.similarity_score > 0.8  # High similarity expected
    
    def test_calculate_similarity_no_match(self):
        """Test similarity calculation with no match"""
        rk = RabinKarpPlagiarism(window_size=3)
        doc_words = ["artificial", "intelligence", "research"]
        ref_words = ["quantum", "computing", "algorithms"]
        
        result = rk.calculate_similarity(doc_words, [ref_words])
        assert result.similarity_score == 0.0
    
    def test_calculate_similarity_partial_match(self, sample_document_words, sample_reference_words):
        """Test similarity calculation with partial match"""
        rk = RabinKarpPlagiarism(window_size=3)
        result = rk.calculate_similarity(sample_document_words, [sample_reference_words])
        assert 0.0 < result.similarity_score < 1.0
    
    def test_calculate_similarity_multiple_references(self):
        """Test similarity with multiple reference documents"""
        rk = RabinKarpPlagiarism(window_size=3)
        doc_words = ["machine", "learning", "algorithms", "analyze", "data"]
        ref1 = ["machine", "learning", "algorithms"]
        ref2 = ["analyze", "data", "efficiently"]
        
        result = rk.calculate_similarity(doc_words, [ref1, ref2])
        assert result.similarity_score > 0.0
        assert result.matched_count > 0
    
    def test_calculate_similarity_empty_document(self):
        """Test similarity with empty document"""
        rk = RabinKarpPlagiarism()
        with pytest.raises(InsufficientDataError):
            rk.calculate_similarity([], [["some", "words"]])
    
    def test_calculate_similarity_empty_references(self):
        """Test similarity with empty references"""
        rk = RabinKarpPlagiarism()
        with pytest.raises(InsufficientDataError):
            rk.calculate_similarity(["some", "words"], [])
    
    def test_result_structure(self, sample_document_words, sample_reference_words):
        """Test result structure completeness"""
        rk = RabinKarpPlagiarism(window_size=3)
        result = rk.calculate_similarity(sample_document_words, [sample_reference_words])
        
        assert hasattr(result, 'similarity_score')
        assert hasattr(result, 'exact_match_score')
        assert hasattr(result, 'matched_windows')
        assert hasattr(result, 'total_windows')
        assert hasattr(result, 'matched_count')
        assert hasattr(result, 'coverage_percentage')
        
        assert isinstance(result.matched_windows, list)
        assert all(isinstance(m, MatchResult) for m in result.matched_windows)
    
    def test_legacy_method(self, sample_document_words, sample_reference_words):
        """Test legacy method for backward compatibility"""
        rk = RabinKarpPlagiarism(window_size=3)
        score, matches = rk.calculate_similarity_legacy(
            sample_document_words,
            [sample_reference_words]
        )
        
        assert isinstance(score, float)
        assert isinstance(matches, list)
        assert 0.0 <= score <= 1.0
    
    def test_hash_collision_handling(self):
        """Test that hash collisions are properly handled"""
        rk = RabinKarpPlagiarism(window_size=3)
        # Create words that might have hash collisions
        doc_words = ["word1", "word2", "word3", "word4"]
        ref_words = ["word1", "word2", "word3", "word5"]
        
        result = rk.calculate_similarity(doc_words, [ref_words])
        # Should detect the matching window despite potential collisions
        assert result.matched_count > 0
