"""
Industry-grade semantic similarity detection using transformer models.
Provides deep semantic understanding for paraphrase detection.
"""
import numpy as np
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from functools import lru_cache
import hashlib

from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings
from utils.logger import get_logger
from utils.exceptions import ModelLoadError, PlagiarismDetectionError, InsufficientDataError

logger = get_logger(__name__)


@dataclass
class SemanticResult:
    """Result from semantic similarity analysis"""
    similarity_score: float
    semantic_similarity_score: float
    max_similarity: float
    min_similarity: float
    avg_similarity: float
    per_sentence_scores: List[float]
    sentence_count: int
    high_similarity_sentences: List[Tuple[str, float]]


class SemanticSimilarity:
    """
    Industry-grade semantic similarity detector using transformer models.
    
    Features:
    - Lazy model loading
    - Embedding caching
    - Batch processing
    - Comprehensive error handling
    - Multiple similarity metrics
    """
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        cache_embeddings: bool = True,
        batch_size: int = 32
    ):
        """
        Initialize semantic similarity detector.
        
        Args:
            model_name: Transformer model name (defaults to settings)
            cache_embeddings: Enable embedding caching
            batch_size: Batch size for encoding
        """
        self.model_name = model_name or settings.semantic_model_name
        self.cache_embeddings = cache_embeddings
        self.batch_size = batch_size
        
        self._model = None
        self._model_loaded = False
        self._embedding_cache: Dict[str, np.ndarray] = {}
        
        logger.info(f"Initialized SemanticSimilarity with model={self.model_name}")
    
    def _load_model(self) -> None:
        """Lazy load the transformer model"""
        if self._model_loaded:
            return
        
        try:
            from sentence_transformers import SentenceTransformer
            
            logger.info(f"Loading transformer model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
            self._model_loaded = True
            logger.info("Model loaded successfully")
            
        except ImportError as e:
            logger.error("sentence-transformers not installed", exc_info=True)
            raise ModelLoadError(
                "sentence-transformers library not installed",
                details={"install_command": "pip install sentence-transformers"}
            )
        except Exception as e:
            logger.error(f"Failed to load model: {e}", exc_info=True)
            raise ModelLoadError(
                f"Failed to load transformer model: {str(e)}",
                details={"model_name": self.model_name}
            )
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _encode_texts(self, texts: List[str]) -> np.ndarray:
        """
        Encode texts to embeddings with caching.
        
        Args:
            texts: List of texts to encode
            
        Returns:
            Numpy array of embeddings
        """
        if not self._model_loaded:
            self._load_model()
        
        if not texts:
            return np.array([])
        
        # Check cache
        if self.cache_embeddings:
            cached_embeddings = []
            uncached_texts = []
            uncached_indices = []
            
            for idx, text in enumerate(texts):
                cache_key = self._get_cache_key(text)
                if cache_key in self._embedding_cache:
                    cached_embeddings.append((idx, self._embedding_cache[cache_key]))
                else:
                    uncached_texts.append(text)
                    uncached_indices.append(idx)
            
            # Encode uncached texts
            if uncached_texts:
                try:
                    new_embeddings = self._model.encode(
                        uncached_texts,
                        batch_size=self.batch_size,
                        show_progress_bar=False,
                        convert_to_numpy=True
                    )
                    
                    # Cache new embeddings
                    for text, embedding in zip(uncached_texts, new_embeddings):
                        cache_key = self._get_cache_key(text)
                        self._embedding_cache[cache_key] = embedding
                    
                    # Combine cached and new embeddings
                    all_embeddings = [None] * len(texts)
                    for idx, emb in cached_embeddings:
                        all_embeddings[idx] = emb
                    for idx, emb in zip(uncached_indices, new_embeddings):
                        all_embeddings[idx] = emb
                    
                    return np.array(all_embeddings)
                    
                except Exception as e:
                    logger.error(f"Encoding error: {e}", exc_info=True)
                    raise PlagiarismDetectionError(
                        f"Failed to encode texts: {str(e)}",
                        details={"text_count": len(uncached_texts)}
                    )
            else:
                # All cached
                return np.array([emb for _, emb in sorted(cached_embeddings)])
        else:
            # No caching
            try:
                return self._model.encode(
                    texts,
                    batch_size=self.batch_size,
                    show_progress_bar=False,
                    convert_to_numpy=True
                )
            except Exception as e:
                logger.error(f"Encoding error: {e}", exc_info=True)
                raise PlagiarismDetectionError(
                    f"Failed to encode texts: {str(e)}",
                    details={"text_count": len(texts)}
                )
    
    def calculate_similarity(
        self,
        doc_sentences: List[str],
        ref_sentences: List[str],
        threshold: float = 0.7
    ) -> SemanticResult:
        """
        Calculate semantic similarity between document and reference sentences.
        
        Args:
            doc_sentences: Document sentences
            ref_sentences: Reference sentences
            threshold: Threshold for high similarity detection
            
        Returns:
            SemanticResult with detailed analysis
            
        Raises:
            InsufficientDataError: If input data is insufficient
            PlagiarismDetectionError: If detection fails
        """
        try:
            # Validation
            if not doc_sentences:
                raise InsufficientDataError("Document sentences are empty")
            
            if not ref_sentences:
                raise InsufficientDataError("Reference sentences are empty")
            
            # Filter empty sentences
            doc_sentences = [s.strip() for s in doc_sentences if s and s.strip()]
            ref_sentences = [s.strip() for s in ref_sentences if s and s.strip()]
            
            if not doc_sentences or not ref_sentences:
                raise InsufficientDataError("All sentences are empty after filtering")
            
            # Encode sentences
            logger.info(f"Encoding {len(doc_sentences)} document and {len(ref_sentences)} reference sentences")
            
            doc_embeddings = self._encode_texts(doc_sentences)
            ref_embeddings = self._encode_texts(ref_sentences)
            
            # Calculate similarities
            similarity_matrix = cosine_similarity(doc_embeddings, ref_embeddings)
            
            # Get max similarity for each document sentence
            per_sentence_scores = np.max(similarity_matrix, axis=1).tolist()
            
            # Calculate metrics
            avg_similarity = float(np.mean(per_sentence_scores))
            max_similarity = float(np.max(per_sentence_scores))
            min_similarity = float(np.min(per_sentence_scores))
            
            # Find high similarity sentences
            high_similarity_sentences = [
                (doc_sentences[i], float(score))
                for i, score in enumerate(per_sentence_scores)
                if score >= threshold
            ]
            
            # Sort by score descending
            high_similarity_sentences.sort(key=lambda x: x[1], reverse=True)
            
            result = SemanticResult(
                similarity_score=round(avg_similarity, 4),
                semantic_similarity_score=round(avg_similarity, 4),
                max_similarity=round(max_similarity, 4),
                min_similarity=round(min_similarity, 4),
                avg_similarity=round(avg_similarity, 4),
                per_sentence_scores=[round(score, 4) for score in per_sentence_scores],
                sentence_count=len(doc_sentences),
                high_similarity_sentences=high_similarity_sentences[:10]  # Top 10
            )
            
            logger.info(
                f"Semantic analysis complete: avg_similarity={avg_similarity:.2%}, "
                f"high_similarity_count={len(high_similarity_sentences)}"
            )
            
            return result
            
        except (InsufficientDataError, ModelLoadError, PlagiarismDetectionError):
            raise
        except Exception as e:
            logger.error(f"Semantic similarity calculation error: {e}", exc_info=True)
            raise PlagiarismDetectionError(
                f"Failed to calculate semantic similarity: {str(e)}",
                details={"error_type": type(e).__name__}
            )
    
    def calculate_similarity_legacy(
        self,
        doc_sentences: List[str],
        ref_sentences: List[str]
    ) -> float:
        """
        Legacy method for backward compatibility.
        
        Returns:
            Similarity score as float
        """
        try:
            if not doc_sentences or not ref_sentences or not self._model_loaded:
                self._load_model()
            
            result = self.calculate_similarity(doc_sentences, ref_sentences)
            return result.similarity_score
        except Exception as e:
            logger.error(f"Legacy semantic calculation failed: {e}")
            return 0.0
    
    def clear_cache(self) -> None:
        """Clear embedding cache"""
        self._embedding_cache.clear()
        logger.info("Embedding cache cleared")
    
    def get_cache_size(self) -> int:
        """Get number of cached embeddings"""
        return len(self._embedding_cache)
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._model_loaded
    
    @property
    def model(self):
        """Get the underlying transformer model"""
        if not self._model_loaded:
            self._load_model()
        return self._model


__all__ = ["SemanticSimilarity", "SemanticResult"]