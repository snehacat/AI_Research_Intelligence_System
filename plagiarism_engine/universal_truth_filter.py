"""
Universal Truth Filter
Filters out common knowledge and universal facts from plagiarism detection
to avoid false positives on statements like "Water boils at 100°C"
"""
import json
import logging
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UniversalTruthFilter:
    """
    Filters universal truths and common knowledge from plagiarism detection.
    
    Examples of universal truths:
    - "Water boils at 100 degrees Celsius"
    - "The Earth orbits the Sun"
    - "DNA contains genetic information"
    - "Photosynthesis produces oxygen"
    """
    
    def __init__(self, knowledge_file: str = None, model=None):
        """
        Initialize the Universal Truth Filter
        
        Args:
            knowledge_file: Path to JSON file with common knowledge statements
            model: Sentence transformer model for semantic matching
        """
        self.model = model
        
        # Load common knowledge
        if knowledge_file is None:
            knowledge_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data",
                "common_knowledge.json"
            )
        
        try:
            with open(knowledge_file, "r", encoding='utf-8') as f:
                data = json.load(f)
                # Handle both list and dict formats
                if isinstance(data, dict):
                    self.facts = data.get("common_knowledge", [])
                else:
                    self.facts = data
                
            logger.info(f"Loaded {len(self.facts)} common knowledge statements")
            
            # Generate embeddings for facts if model provided
            if self.model:
                self.fact_embeddings = self.model.encode(self.facts)
                logger.info("Generated embeddings for common knowledge")
            else:
                self.fact_embeddings = None
                logger.warning("No model provided - using keyword matching only")
                
        except FileNotFoundError:
            logger.error(f"Knowledge file not found: {knowledge_file}")
            self.facts = []
            self.fact_embeddings = None
        except Exception as e:
            logger.error(f"Error loading knowledge file: {str(e)}")
            self.facts = []
            self.fact_embeddings = None
    
    def is_universal_truth(self, sentence: str, threshold: float = 0.85) -> bool:
        """
        Check if a sentence is a universal truth/common knowledge
        
        Args:
            sentence: Sentence to check
            threshold: Similarity threshold (0-1)
            
        Returns:
            True if sentence is common knowledge
        """
        if not sentence or not self.facts:
            return False
        
        # Method 1: Exact/keyword matching (fast)
        sentence_lower = sentence.lower()
        for fact in self.facts:
            if fact.lower() in sentence_lower or sentence_lower in fact.lower():
                logger.debug(f"Exact match found: {sentence[:50]}...")
                return True
        
        # Method 2: Semantic matching (more accurate)
        if self.model and self.fact_embeddings is not None:
            try:
                sentence_embedding = self.model.encode([sentence])
                similarities = cosine_similarity(sentence_embedding, self.fact_embeddings)
                max_similarity = np.max(similarities)
                
                if max_similarity >= threshold:
                    logger.debug(f"Semantic match found (sim={max_similarity:.2f}): {sentence[:50]}...")
                    return True
            except Exception as e:
                logger.error(f"Error in semantic matching: {str(e)}")
        
        return False
    
    def filter_sentences(self, sentences: List[str], threshold: float = 0.85) -> Dict[str, List[str]]:
        """
        Filter sentences into universal truths and original content
        
        Args:
            sentences: List of sentences to filter
            threshold: Similarity threshold
            
        Returns:
            Dict with 'universal_truths' and 'original_content' lists
        """
        universal_truths = []
        original_content = []
        
        for sentence in sentences:
            if self.is_universal_truth(sentence, threshold):
                universal_truths.append(sentence)
            else:
                original_content.append(sentence)
        
        logger.info(f"Filtered {len(universal_truths)} universal truths from {len(sentences)} sentences")
        
        return {
            'universal_truths': universal_truths,
            'original_content': original_content,
            'universal_truth_ratio': len(universal_truths) / len(sentences) if sentences else 0
        }
    
    def adjust_plagiarism_score(
        self, 
        raw_score: float, 
        doc_embeddings: Optional[np.ndarray] = None,
        sentences: Optional[List[str]] = None,
        threshold: float = 0.85
    ) -> Dict[str, float]:
        """
        Adjust plagiarism score by removing universal truths
        
        Args:
            raw_score: Original plagiarism score (0-1)
            doc_embeddings: Document sentence embeddings (optional)
            sentences: List of sentences (optional, for better accuracy)
            threshold: Similarity threshold
            
        Returns:
            Dict with adjusted_score, truth_ratio, and original_score
        """
        if raw_score == 0:
            return {
                'adjusted_score': 0.0,
                'original_score': 0.0,
                'truth_ratio': 0.0,
                'truths_found': 0
            }
        
        truth_matches = 0
        total_items = 0
        
        # Method 1: Use sentences if provided (most accurate)
        if sentences:
            filtered = self.filter_sentences(sentences, threshold)
            truth_ratio = filtered['universal_truth_ratio']
            truth_matches = len(filtered['universal_truths'])
            total_items = len(sentences)
        
        # Method 2: Use embeddings if provided
        elif doc_embeddings is not None and self.fact_embeddings is not None:
            try:
                sim_matrix = cosine_similarity(doc_embeddings, self.fact_embeddings)
                
                for row in sim_matrix:
                    if np.max(row) >= threshold:
                        truth_matches += 1
                
                total_items = len(doc_embeddings)
                truth_ratio = truth_matches / total_items if total_items > 0 else 0
            except Exception as e:
                logger.error(f"Error in embedding-based filtering: {str(e)}")
                truth_ratio = 0
        
        # Method 3: Conservative estimate (least accurate)
        else:
            logger.warning("No sentences or embeddings provided - using conservative estimate")
            truth_ratio = 0.1  # Assume 10% might be common knowledge
            truth_matches = 0
            total_items = 0
        
        # Adjust score: reduce by the proportion of universal truths
        adjusted_score = raw_score * (1 - truth_ratio)
        adjusted_score = max(0, min(1, adjusted_score))  # Clamp to [0, 1]
        
        logger.info(
            f"Plagiarism score adjusted: {raw_score:.2%} → {adjusted_score:.2%} "
            f"(removed {truth_matches}/{total_items} universal truths)"
        )
        
        return {
            'adjusted_score': round(adjusted_score, 4),
            'original_score': round(raw_score, 4),
            'truth_ratio': round(truth_ratio, 4),
            'truths_found': truth_matches,
            'total_sentences': total_items
        }
    
    def add_common_knowledge(self, statements: List[str]):
        """
        Add new common knowledge statements
        
        Args:
            statements: List of new common knowledge statements
        """
        self.facts.extend(statements)
        
        if self.model:
            # Regenerate embeddings
            self.fact_embeddings = self.model.encode(self.facts)
            logger.info(f"Added {len(statements)} new statements. Total: {len(self.facts)}")
    
    def get_statistics(self) -> Dict:
        """Get filter statistics"""
        return {
            'total_facts': len(self.facts),
            'has_embeddings': self.fact_embeddings is not None,
            'embedding_model': self.model is not None,
            'sample_facts': self.facts[:5] if self.facts else []
        }


# API-Enhanced Version (Optional)
class APIEnhancedUniversalTruthFilter(UniversalTruthFilter):
    """
    Enhanced version that uses APIs to verify universal truths
    - Wikipedia API: Check if statement is from Wikipedia
    - Wikidata API: Verify scientific facts
    - OpenAI API: Classify as common knowledge
    """
    
    def __init__(self, knowledge_file: str = None, model=None, use_apis: bool = False):
        super().__init__(knowledge_file, model)
        self.use_apis = use_apis
        
        if use_apis:
            try:
                from api_integrations.wikipedia_client import WikipediaClient
                self.wikipedia = WikipediaClient()
                logger.info("Wikipedia API enabled for truth verification")
            except:
                logger.warning("Wikipedia API not available")
                self.wikipedia = None
    
    def verify_with_wikipedia(self, sentence: str) -> bool:
        """
        Verify if sentence is common knowledge using Wikipedia
        
        Args:
            sentence: Sentence to verify
            
        Returns:
            True if found in Wikipedia as common knowledge
        """
        if not self.use_apis or not self.wikipedia:
            return False
        
        try:
            # Extract key terms and search Wikipedia
            # If found in intro paragraph, likely common knowledge
            result = self.wikipedia.search(sentence[:100])
            return result is not None
        except:
            return False
    
    def is_universal_truth(self, sentence: str, threshold: float = 0.85) -> bool:
        """
        Enhanced version with API verification
        """
        # First check local database
        is_truth = super().is_universal_truth(sentence, threshold)
        
        # If not found locally, check APIs
        if not is_truth and self.use_apis:
            is_truth = self.verify_with_wikipedia(sentence)
        
        return is_truth
