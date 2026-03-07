"""
Industry-grade TF-IDF based lexical similarity detection.
Uses n-gram analysis and cosine similarity for paraphrase detection.
"""
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings
from utils.logger import get_logger
from utils.exceptions import PlagiarismDetectionError, InsufficientDataError

logger = get_logger(__name__)


@dataclass
class TFIDFResult:
    """Result from TF-IDF analysis"""
    similarity_score: float
    lexical_similarity_score: float
    max_similarity: float
    min_similarity: float
    avg_similarity: float
    per_reference_scores: List[float]
    feature_count: int
    top_features: List[Tuple[str, float]]


class TFIDFSimilarity:
    """
    Industry-grade TF-IDF similarity detector for lexical plagiarism.
    
    Features:
    - Configurable n-gram ranges
    - Multiple similarity metrics
    - Feature importance analysis
    - Robust error handling
    - Performance optimization
    """
    
    def __init__(
        self,
        ngram_range: Optional[Tuple[int, int]] = None,
        max_features: int = 10000,
        min_df: int = 1,
        max_df: float = 0.95,
        use_idf: bool = True,
        sublinear_tf: bool = True
    ):
        """
        Initialize TF-IDF similarity detector.
        
        Args:
            ngram_range: Range of n-grams (defaults to settings)
            max_features: Maximum number of features
            min_df: Minimum document frequency
            max_df: Maximum document frequency (as ratio)
            use_idf: Use inverse document frequency weighting
            sublinear_tf: Apply sublinear tf scaling
        """
        self.ngram_range = ngram_range or settings.tfidf_ngram_range
        self.max_features = max_features
        self.min_df = min_df
        self.max_df = max_df
        
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=self.ngram_range,
            max_features=self.max_features,
            min_df=self.min_df,
            max_df=self.max_df,
            use_idf=use_idf,
            sublinear_tf=sublinear_tf,
            lowercase=True,
            strip_accents='unicode',
            token_pattern=r'\b\w+\b'
        )
        
        self._is_fitted = False
        
        logger.info(
            f"Initialized TF-IDF with ngram_range={self.ngram_range}, "
            f"max_features={self.max_features}"
        )
    
    def _get_top_features(
        self,
        tfidf_matrix: np.ndarray,
        feature_names: List[str],
        top_n: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Get top TF-IDF features for the document.
        
        Args:
            tfidf_matrix: TF-IDF matrix
            feature_names: Feature names from vectorizer
            top_n: Number of top features to return
            
        Returns:
            List of (feature, score) tuples
        """
        try:
            # Get document vector (first row)
            doc_vector = tfidf_matrix[0].toarray().flatten()
            
            # Get top indices
            top_indices = doc_vector.argsort()[-top_n:][::-1]
            
            # Get feature names and scores
            top_features = [
                (feature_names[idx], float(doc_vector[idx]))
                for idx in top_indices
                if doc_vector[idx] > 0
            ]
            
            return top_features
        except Exception as e:
            logger.warning(f"Failed to extract top features: {e}")
            return []
    
    def calculate_similarity(
        self,
        doc_text: str,
        ref_texts: List[str],
        return_detailed: bool = True
    ) -> TFIDFResult:
        """
        Calculate TF-IDF based lexical similarity.
        
        Args:
            doc_text: Document text
            ref_texts: List of reference texts
            return_detailed: If True, return detailed analysis
            
        Returns:
            TFIDFResult with analysis
            
        Raises:
            InsufficientDataError: If input data is insufficient
            PlagiarismDetectionError: If detection fails
        """
        try:
            # Validation
            if not doc_text or not doc_text.strip():
                raise InsufficientDataError("Document text is empty")
            
            if not ref_texts:
                raise InsufficientDataError("Reference corpus is empty")
            
            # Filter empty references
            ref_texts = [ref for ref in ref_texts if ref and ref.strip()]
            
            if not ref_texts:
                raise InsufficientDataError("All reference texts are empty")
            
            # Combine into corpus
            corpus = [doc_text] + ref_texts
            
            # Fit and transform
            try:
                tfidf_matrix = self.vectorizer.fit_transform(corpus)
                self._is_fitted = True
            except ValueError as e:
                logger.error(f"TF-IDF vectorization failed: {e}")
                raise PlagiarismDetectionError(
                    "Failed to vectorize text - insufficient vocabulary",
                    details={"error": str(e)}
                )
            
            # Calculate similarities
            doc_vector = tfidf_matrix[0:1]
            ref_vectors = tfidf_matrix[1:]
            
            similarities = cosine_similarity(doc_vector, ref_vectors).flatten()
            
            # Calculate metrics
            per_reference_scores = [float(score) for score in similarities]
            avg_similarity = float(np.mean(similarities))
            max_similarity = float(np.max(similarities))
            min_similarity = float(np.min(similarities))
            
            # Get top features if detailed analysis requested
            top_features = []
            if return_detailed:
                feature_names = self.vectorizer.get_feature_names_out()
                top_features = self._get_top_features(tfidf_matrix, feature_names)
            
            result = TFIDFResult(
                similarity_score=round(avg_similarity, 4),
                lexical_similarity_score=round(avg_similarity, 4),
                max_similarity=round(max_similarity, 4),
                min_similarity=round(min_similarity, 4),
                avg_similarity=round(avg_similarity, 4),
                per_reference_scores=[round(score, 4) for score in per_reference_scores],
                feature_count=tfidf_matrix.shape[1],
                top_features=top_features
            )
            
            logger.info(
                f"TF-IDF analysis complete: avg_similarity={avg_similarity:.2%}, "
                f"features={result.feature_count}"
            )
            
            return result
            
        except (InsufficientDataError, PlagiarismDetectionError):
            raise
        except Exception as e:
            logger.error(f"TF-IDF calculation error: {e}", exc_info=True)
            raise PlagiarismDetectionError(
                f"Failed to calculate TF-IDF similarity: {str(e)}",
                details={"error_type": type(e).__name__}
            )
    
    def calculate_similarity_legacy(
        self,
        doc_text: str,
        ref_texts: List[str]
    ) -> Dict[str, float]:
        """
        Legacy method for backward compatibility.
        
        Returns:
            Dictionary with 'score' key
        """
        try:
            result = self.calculate_similarity(doc_text, ref_texts, return_detailed=False)
            return {"score": result.similarity_score}
        except Exception as e:
            logger.error(f"Legacy TF-IDF calculation failed: {e}")
            return {"score": 0.0}
    
    def is_fitted(self) -> bool:
        """Check if vectorizer has been fitted"""
        return self._is_fitted
    
    def get_vocabulary_size(self) -> int:
        """Get size of learned vocabulary"""
        if not self._is_fitted:
            return 0
        return len(self.vectorizer.vocabulary_)


__all__ = ["TFIDFSimilarity", "TFIDFResult"]