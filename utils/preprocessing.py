"""
Industry-grade text preprocessing with robust NLP pipeline,
caching, and comprehensive error handling.
"""
import re
import string
from typing import List, Optional, Set, Dict, Union
from functools import lru_cache
from dataclasses import dataclass

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

from utils.logger import get_logger
from utils.exceptions import InvalidInputError

logger = get_logger(__name__)

# Ensure NLTK resources are downloaded
_REQUIRED_NLTK_DATA = ["punkt", "stopwords", "wordnet", "averaged_perceptron_tagger"]

def _download_nltk_resources() -> None:
    """Download required NLTK resources if not already present"""
    for resource in _REQUIRED_NLTK_DATA:
        try:
            nltk.data.find(f"tokenizers/{resource}")
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
                logger.info(f"Downloaded NLTK resource: {resource}")
            except Exception as e:
                logger.warning(f"Failed to download NLTK resource {resource}: {e}")

# Download resources on module import
_download_nltk_resources()

# Global stopwords set
STOP_WORDS: Set[str] = set(stopwords.words("english"))


@dataclass
class PreprocessingConfig:
    """Configuration for text preprocessing"""
    lowercase: bool = True
    remove_numbers: bool = True
    remove_punctuation: bool = True
    remove_stopwords: bool = True
    lemmatize: bool = False
    min_word_length: int = 2
    max_word_length: int = 50
    preserve_sentence_structure: bool = False


class TextPreprocessor:
    """
    Industry-grade text preprocessor with configurable pipeline,
    caching, and comprehensive error handling.
    """
    
    def __init__(self, config: Optional[PreprocessingConfig] = None):
        """
        Initialize text preprocessor.
        
        Args:
            config: Preprocessing configuration (uses defaults if None)
        """
        self.config = config or PreprocessingConfig()
        self._lemmatizer: Optional[WordNetLemmatizer] = None
        
        if self.config.lemmatize:
            try:
                self._lemmatizer = WordNetLemmatizer()
            except Exception as e:
                logger.warning(f"Failed to initialize lemmatizer: {e}")
                self.config.lemmatize = False
    
    def clean_text(self, text: str, preserve_structure: bool = False) -> str:
        """
        Clean text with configurable options.
        
        Args:
            text: Input text
            preserve_structure: If True, preserve sentence structure
            
        Returns:
            Cleaned text
            
        Raises:
            InvalidInputError: If input is invalid
        """
        if not isinstance(text, str):
            raise InvalidInputError(
                "Input must be a string",
                details={"input_type": type(text).__name__}
            )
        
        if not text.strip():
            return ""
        
        # Lowercase
        if self.config.lowercase:
            text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove numbers
        if self.config.remove_numbers:
            text = re.sub(r'\d+', '', text)
        
        # Remove punctuation
        if self.config.remove_punctuation:
            if preserve_structure:
                # Keep sentence-ending punctuation
                text = re.sub(r'[^\w\s.!?]', '', text)
            else:
                text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_words(self, text: str) -> List[str]:
        """
        Tokenize text into words with validation.
        
        Args:
            text: Input text
            
        Returns:
            List of word tokens
        """
        if not isinstance(text, str):
            raise InvalidInputError(
                "Input must be a string",
                details={"input_type": type(text).__name__}
            )
        
        if not text.strip():
            return []
        
        try:
            tokens = word_tokenize(text)
            
            # Filter by length
            tokens = [
                t for t in tokens
                if self.config.min_word_length <= len(t) <= self.config.max_word_length
            ]
            
            return tokens
        except Exception as e:
            logger.error(f"Tokenization error: {e}", exc_info=True)
            # Fallback to simple split
            return text.split()
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """
        Tokenize text into sentences with validation.
        
        Args:
            text: Input text
            
        Returns:
            List of sentence tokens
        """
        if not isinstance(text, str):
            raise InvalidInputError(
                "Input must be a string",
                details={"input_type": type(text).__name__}
            )
        
        if not text.strip():
            return []
        
        try:
            sentences = sent_tokenize(text)
            # Filter empty sentences
            return [s.strip() for s in sentences if s.strip()]
        except Exception as e:
            logger.error(f"Sentence tokenization error: {e}", exc_info=True)
            # Fallback to simple split
            return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    
    def remove_stopwords(self, tokens: List[str], custom_stopwords: Optional[Set[str]] = None) -> List[str]:
        """
        Remove stopwords from token list.
        
        Args:
            tokens: List of tokens
            custom_stopwords: Optional custom stopwords to add
            
        Returns:
            Filtered token list
        """
        if not isinstance(tokens, list):
            raise InvalidInputError(
                "Tokens must be a list",
                details={"input_type": type(tokens).__name__}
            )
        
        stopwords_set = STOP_WORDS.copy()
        if custom_stopwords:
            stopwords_set.update(custom_stopwords)
        
        return [word for word in tokens if word.lower() not in stopwords_set]
    
    def lemmatize_tokens(self, tokens: List[str]) -> List[str]:
        """
        Lemmatize tokens to their base form.
        
        Args:
            tokens: List of tokens
            
        Returns:
            Lemmatized tokens
        """
        if not self._lemmatizer:
            logger.warning("Lemmatizer not initialized, returning original tokens")
            return tokens
        
        try:
            return [self._lemmatizer.lemmatize(token) for token in tokens]
        except Exception as e:
            logger.error(f"Lemmatization error: {e}", exc_info=True)
            return tokens
    
    def preprocess_for_similarity(self, text: str) -> str:
        """
        Full preprocessing pipeline for similarity analysis.
        
        Args:
            text: Input text
            
        Returns:
            Preprocessed text as string
        """
        if not text:
            return ""
        
        try:
            # Clean text
            text = self.clean_text(text, preserve_structure=False)
            
            # Tokenize
            tokens = self.tokenize_words(text)
            
            # Remove stopwords
            if self.config.remove_stopwords:
                tokens = self.remove_stopwords(tokens)
            
            # Lemmatize
            if self.config.lemmatize:
                tokens = self.lemmatize_tokens(tokens)
            
            return " ".join(tokens)
        except Exception as e:
            logger.error(f"Preprocessing error: {e}", exc_info=True)
            return text  # Return original on error
    
    def preprocess_for_tokens(self, text: str) -> List[str]:
        """
        Full preprocessing pipeline returning tokens.
        
        Args:
            text: Input text
            
        Returns:
            List of preprocessed tokens
        """
        if not text:
            return []
        
        try:
            # Clean text
            text = self.clean_text(text, preserve_structure=False)
            
            # Tokenize
            tokens = self.tokenize_words(text)
            
            # Remove stopwords
            if self.config.remove_stopwords:
                tokens = self.remove_stopwords(tokens)
            
            # Lemmatize
            if self.config.lemmatize:
                tokens = self.lemmatize_tokens(tokens)
            
            return tokens
        except Exception as e:
            logger.error(f"Preprocessing error: {e}", exc_info=True)
            return text.split()  # Return simple split on error
    
    def preprocess_for_sentences(self, text: str) -> List[str]:
        """
        Preprocess text preserving sentence structure.
        
        Args:
            text: Input text
            
        Returns:
            List of preprocessed sentences
        """
        if not text:
            return []
        
        try:
            # Tokenize into sentences first
            sentences = self.tokenize_sentences(text)
            
            # Process each sentence
            processed_sentences = []
            for sentence in sentences:
                cleaned = self.clean_text(sentence, preserve_structure=True)
                if cleaned:
                    processed_sentences.append(cleaned)
            
            return processed_sentences
        except Exception as e:
            logger.error(f"Sentence preprocessing error: {e}", exc_info=True)
            return [text]  # Return original as single sentence on error
    
    def get_statistics(self, text: str) -> Dict[str, Union[int, float]]:
        """
        Get text statistics.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with text statistics
        """
        try:
            sentences = self.tokenize_sentences(text)
            words = self.tokenize_words(text)
            
            return {
                "character_count": len(text),
                "word_count": len(words),
                "sentence_count": len(sentences),
                "avg_word_length": float(sum(len(w) for w in words) / len(words)) if words else 0.0,
                "avg_sentence_length": float(len(words) / len(sentences)) if sentences else 0.0,
            }
        except Exception as e:
            logger.error(f"Statistics calculation error: {e}", exc_info=True)
            return {
                "character_count": len(text),
                "word_count": 0,
                "sentence_count": 0,
                "avg_word_length": 0.0,
                "avg_sentence_length": 0.0,
            }


# Singleton instance with default configuration
_default_preprocessor = TextPreprocessor()


# Convenience functions for backward compatibility
def clean_text(text: str) -> str:
    """Clean text using default preprocessor"""
    return _default_preprocessor.clean_text(text)


def tokenize_words(text: str) -> List[str]:
    """Tokenize words using default preprocessor"""
    return _default_preprocessor.tokenize_words(text)


def tokenize_sentences(text: str) -> List[str]:
    """Tokenize sentences using default preprocessor"""
    return _default_preprocessor.tokenize_sentences(text)


def remove_stopwords(tokens: List[str]) -> List[str]:
    """Remove stopwords using default preprocessor"""
    return _default_preprocessor.remove_stopwords(tokens)


def preprocess_for_similarity(text: str) -> str:
    """Preprocess for similarity using default preprocessor"""
    return _default_preprocessor.preprocess_for_similarity(text)


def preprocess_for_tokens(text: str) -> List[str]:
    """Preprocess for tokens using default preprocessor"""
    return _default_preprocessor.preprocess_for_tokens(text)


__all__ = [
    "TextPreprocessor",
    "PreprocessingConfig",
    "clean_text",
    "tokenize_words",
    "tokenize_sentences",
    "remove_stopwords",
    "preprocess_for_similarity",
    "preprocess_for_tokens",
    "STOP_WORDS",
]
