"""
Tests for text preprocessing utilities.
"""
import pytest
from utils.preprocessing import (
    TextPreprocessor,
    PreprocessingConfig,
    clean_text,
    tokenize_words,
    tokenize_sentences,
    remove_stopwords,
)
from utils.exceptions import InvalidInputError


class TestTextPreprocessor:
    """Test TextPreprocessor class"""
    
    def test_initialization_default(self):
        """Test default initialization"""
        preprocessor = TextPreprocessor()
        assert preprocessor.config.lowercase is True
        assert preprocessor.config.remove_stopwords is True
    
    def test_initialization_custom_config(self):
        """Test initialization with custom config"""
        config = PreprocessingConfig(lowercase=False, lemmatize=True)
        preprocessor = TextPreprocessor(config)
        assert preprocessor.config.lowercase is False
        assert preprocessor.config.lemmatize is True
    
    def test_clean_text_basic(self, sample_text):
        """Test basic text cleaning"""
        preprocessor = TextPreprocessor()
        cleaned = preprocessor.clean_text(sample_text)
        assert cleaned.islower()
        assert not any(char.isdigit() for char in cleaned)
    
    def test_clean_text_with_urls(self):
        """Test URL removal"""
        preprocessor = TextPreprocessor()
        text = "Check this link https://example.com for more info"
        cleaned = preprocessor.clean_text(text)
        assert "https://example.com" not in cleaned
        assert "example.com" not in cleaned
    
    def test_clean_text_with_emails(self):
        """Test email removal"""
        preprocessor = TextPreprocessor()
        text = "Contact us at test@example.com for details"
        cleaned = preprocessor.clean_text(text)
        assert "test@example.com" not in cleaned
    
    def test_clean_text_empty(self, empty_text):
        """Test cleaning empty text"""
        preprocessor = TextPreprocessor()
        cleaned = preprocessor.clean_text(empty_text)
        assert cleaned == ""
    
    def test_clean_text_invalid_input(self):
        """Test cleaning with invalid input"""
        preprocessor = TextPreprocessor()
        with pytest.raises(InvalidInputError):
            preprocessor.clean_text(123)
    
    def test_tokenize_words(self, sample_text):
        """Test word tokenization"""
        preprocessor = TextPreprocessor()
        tokens = preprocessor.tokenize_words(sample_text)
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        assert all(isinstance(token, str) for token in tokens)
    
    def test_tokenize_words_empty(self, empty_text):
        """Test word tokenization with empty text"""
        preprocessor = TextPreprocessor()
        tokens = preprocessor.tokenize_words(empty_text)
        assert tokens == []
    
    def test_tokenize_sentences(self, sample_text):
        """Test sentence tokenization"""
        preprocessor = TextPreprocessor()
        sentences = preprocessor.tokenize_sentences(sample_text)
        assert isinstance(sentences, list)
        assert len(sentences) > 0
    
    def test_remove_stopwords(self):
        """Test stopword removal"""
        preprocessor = TextPreprocessor()
        tokens = ["the", "quick", "brown", "fox", "is", "fast"]
        filtered = preprocessor.remove_stopwords(tokens)
        assert "the" not in filtered
        assert "is" not in filtered
        assert "quick" in filtered
        assert "fox" in filtered
    
    def test_preprocess_for_similarity(self, sample_text):
        """Test full preprocessing pipeline"""
        preprocessor = TextPreprocessor()
        processed = preprocessor.preprocess_for_similarity(sample_text)
        assert isinstance(processed, str)
        assert len(processed) > 0
        assert processed.islower()
    
    def test_preprocess_for_tokens(self, sample_text):
        """Test preprocessing returning tokens"""
        preprocessor = TextPreprocessor()
        tokens = preprocessor.preprocess_for_tokens(sample_text)
        assert isinstance(tokens, list)
        assert len(tokens) > 0
    
    def test_get_statistics(self, sample_text):
        """Test text statistics calculation"""
        preprocessor = TextPreprocessor()
        stats = preprocessor.get_statistics(sample_text)
        assert "character_count" in stats
        assert "word_count" in stats
        assert "sentence_count" in stats
        assert stats["word_count"] > 0


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    def test_clean_text_function(self, sample_text):
        """Test clean_text convenience function"""
        cleaned = clean_text(sample_text)
        assert isinstance(cleaned, str)
        assert cleaned.islower()
    
    def test_tokenize_words_function(self, sample_text):
        """Test tokenize_words convenience function"""
        tokens = tokenize_words(sample_text)
        assert isinstance(tokens, list)
        assert len(tokens) > 0
    
    def test_tokenize_sentences_function(self, sample_text):
        """Test tokenize_sentences convenience function"""
        sentences = tokenize_sentences(sample_text)
        assert isinstance(sentences, list)
        assert len(sentences) > 0
    
    def test_remove_stopwords_function(self):
        """Test remove_stopwords convenience function"""
        tokens = ["the", "quick", "brown", "fox"]
        filtered = remove_stopwords(tokens)
        assert "the" not in filtered
        assert "quick" in filtered
