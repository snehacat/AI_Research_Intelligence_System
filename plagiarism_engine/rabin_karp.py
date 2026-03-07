"""
Industry-grade Rabin-Karp algorithm implementation for exact match plagiarism detection.
Uses rolling hash for efficient string matching with configurable window sizes.
"""
import re
from typing import Set, List, Tuple, Dict, Optional
from dataclasses import dataclass
from collections import defaultdict

from utils.logger import get_logger
from utils.exceptions import PlagiarismDetectionError, InsufficientDataError

logger = get_logger(__name__)


@dataclass
class MatchResult:
    """Result of a plagiarism match"""
    matched_text: str
    position: int
    source_id: Optional[str] = None
    confidence: float = 1.0


@dataclass
class RabinKarpResult:
    """Complete result from Rabin-Karp analysis"""
    similarity_score: float
    exact_match_score: float
    matched_windows: List[MatchResult]
    total_windows: int
    matched_count: int
    coverage_percentage: float


class RabinKarpPlagiarism:
    """
    Industry-grade Rabin-Karp plagiarism detector with rolling hash.
    
    Features:
    - Efficient O(n) rolling hash computation
    - Configurable window sizes
    - Detailed match reporting
    - Hash collision handling
    - Performance optimizations
    """
    
    # Prime number for hash calculation (large prime reduces collisions)
    HASH_PRIME = 101
    HASH_MOD = 10**9 + 7
    
    def __init__(
        self,
        window_size: int = 5,
        min_window_size: int = 3,
        max_window_size: int = 15,
        enable_variable_windows: bool = False
    ):
        """
        Initialize Rabin-Karp plagiarism detector.
        
        Args:
            window_size: Default window size for fingerprinting
            min_window_size: Minimum window size (for validation)
            max_window_size: Maximum window size (for validation)
            enable_variable_windows: If True, use multiple window sizes
        """
        if not (min_window_size <= window_size <= max_window_size):
            raise ValueError(
                f"Window size {window_size} must be between {min_window_size} and {max_window_size}"
            )
        
        self.window_size = window_size
        self.min_window_size = min_window_size
        self.max_window_size = max_window_size
        self.enable_variable_windows = enable_variable_windows
        
        logger.info(
            f"Initialized Rabin-Karp with window_size={window_size}, "
            f"variable_windows={enable_variable_windows}"
        )
    
    def _compute_hash(self, words: Tuple[str, ...]) -> int:
        """
        Compute hash for a window of words using polynomial rolling hash.
        
        Args:
            words: Tuple of words
            
        Returns:
            Hash value
        """
        hash_value = 0
        for i, word in enumerate(words):
            # Use word hash and position for better distribution
            word_hash = hash(word.lower())
            hash_value = (hash_value + word_hash * pow(self.HASH_PRIME, i, self.HASH_MOD)) % self.HASH_MOD
        return hash_value
    
    def generate_fingerprints(
        self,
        words: List[str],
        window_size: Optional[int] = None
    ) -> Dict[int, List[Tuple[str, ...]]]:
        """
        Generate fingerprints (hashes) for all windows in the text.
        Returns dict mapping hash -> list of actual word tuples (for collision handling).
        
        Args:
            words: List of words
            window_size: Window size (uses default if None)
            
        Returns:
            Dictionary mapping hash values to word tuples
        """
        ws = window_size or self.window_size
        fingerprints: Dict[int, List[Tuple[str, ...]]] = defaultdict(list)
        
        if len(words) < ws:
            logger.warning(f"Text too short ({len(words)} words) for window size {ws}")
            return fingerprints
        
        # Generate fingerprints for all windows
        for i in range(len(words) - ws + 1):
            window = tuple(words[i:i + ws])
            window_hash = self._compute_hash(window)
            fingerprints[window_hash].append(window)
        
        return fingerprints
    
    def _verify_match(self, window1: Tuple[str, ...], window2: Tuple[str, ...]) -> bool:
        """
        Verify that two windows actually match (handle hash collisions).
        
        Args:
            window1: First window
            window2: Second window
            
        Returns:
            True if windows match exactly
        """
        if len(window1) != len(window2):
            return False
        return all(w1.lower() == w2.lower() for w1, w2 in zip(window1, window2))
    
    def calculate_similarity(
        self,
        doc_words: List[str],
        ref_words_list: List[List[str]],
        source_ids: Optional[List[str]] = None
    ) -> RabinKarpResult:
        """
        Calculate exact match similarity between document and reference corpus.
        
        Args:
            doc_words: Document words
            ref_words_list: List of reference document word lists
            source_ids: Optional source identifiers for references
            
        Returns:
            RabinKarpResult with detailed analysis
            
        Raises:
            InsufficientDataError: If input data is insufficient
            PlagiarismDetectionError: If detection fails
        """
        try:
            # Validation
            if not doc_words:
                raise InsufficientDataError("Document is empty")
            
            if not ref_words_list:
                raise InsufficientDataError("Reference corpus is empty")
            
            # Generate document fingerprints
            doc_fps = self.generate_fingerprints(doc_words)
            
            if not doc_fps:
                logger.warning("No fingerprints generated from document")
                return RabinKarpResult(
                    similarity_score=0.0,
                    exact_match_score=0.0,
                    matched_windows=[],
                    total_windows=0,
                    matched_count=0,
                    coverage_percentage=0.0
                )
            
            # Generate reference fingerprints
            ref_fps: Dict[int, List[Tuple[Tuple[str, ...], Optional[str]]]] = defaultdict(list)
            
            for idx, ref_words in enumerate(ref_words_list):
                source_id = source_ids[idx] if source_ids and idx < len(source_ids) else None
                ref_fingerprints = self.generate_fingerprints(ref_words)
                
                for hash_val, windows in ref_fingerprints.items():
                    for window in windows:
                        ref_fps[hash_val].append((window, source_id))
            
            # Find matches with collision handling
            matched_windows: List[MatchResult] = []
            matched_hashes: Set[int] = set()
            
            for i in range(len(doc_words) - self.window_size + 1):
                doc_window = tuple(doc_words[i:i + self.window_size])
                doc_hash = self._compute_hash(doc_window)
                
                if doc_hash in ref_fps and doc_hash not in matched_hashes:
                    # Verify match (handle collisions)
                    for ref_window, source_id in ref_fps[doc_hash]:
                        if self._verify_match(doc_window, ref_window):
                            matched_windows.append(
                                MatchResult(
                                    matched_text=' '.join(doc_window),
                                    position=i,
                                    source_id=source_id,
                                    confidence=1.0
                                )
                            )
                            matched_hashes.add(doc_hash)
                            break
            
            # Calculate scores
            total_windows = len(doc_fps)
            matched_count = len(matched_hashes)
            similarity_score = matched_count / total_windows if total_windows > 0 else 0.0
            
            # Calculate coverage (percentage of document that matches)
            coverage_percentage = (matched_count * self.window_size) / len(doc_words) * 100 if doc_words else 0.0
            
            result = RabinKarpResult(
                similarity_score=round(similarity_score, 4),
                exact_match_score=round(similarity_score, 4),  # Same for Rabin-Karp
                matched_windows=matched_windows[:20],  # Top 20 matches
                total_windows=total_windows,
                matched_count=matched_count,
                coverage_percentage=round(coverage_percentage, 2)
            )
            
            logger.info(
                f"Rabin-Karp analysis complete: {matched_count}/{total_windows} windows matched "
                f"({result.similarity_score:.2%})"
            )
            
            return result
            
        except (InsufficientDataError, PlagiarismDetectionError):
            raise
        except Exception as e:
            logger.error(f"Rabin-Karp calculation error: {e}", exc_info=True)
            raise PlagiarismDetectionError(
                f"Failed to calculate similarity: {str(e)}",
                details={"error_type": type(e).__name__}
            )
    
    def calculate_similarity_legacy(
        self,
        doc_words: List[str],
        ref_words_list: List[List[str]]
    ) -> Tuple[float, List[str]]:
        """
        Legacy method for backward compatibility.
        
        Returns:
            Tuple of (similarity_score, matched_windows_list)
        """
        result = self.calculate_similarity(doc_words, ref_words_list)
        matched_texts = [match.matched_text for match in result.matched_windows[:5]]
        return result.similarity_score, matched_texts


__all__ = ["RabinKarpPlagiarism", "RabinKarpResult", "MatchResult"]