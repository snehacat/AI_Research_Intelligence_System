"""
Industry-grade unified scoring engine that orchestrates all analysis components.
"""
from typing import List, Dict, Optional, Any
import re
from dataclasses import dataclass, asdict

from app.config import settings
from utils.logger import get_logger
from utils.preprocessing import TextPreprocessor
from utils.exceptions import AnalysisError, InsufficientDataError

from plagiarism_engine.rabin_karp import RabinKarpPlagiarism
from plagiarism_engine.tfidf_engine import TFIDFSimilarity
from plagiarism_engine.semantic_engine import SemanticSimilarity
from plagiarism_engine.universal_truth_filter import UniversalTruthFilter

logger = get_logger(__name__)


@dataclass
class AnalysisResult:
    """Complete analysis result"""
    plagiarism_analysis: Dict[str, Any]
    quality_analysis: Dict[str, Any]
    final_scores: Dict[str, float]
    statistics: Dict[str, Any]
    recommendations: List[str]


class ToneChecker:
    """Basic tone analysis (placeholder for now)"""
    
    def analyze(self, doc: str) -> Dict[str, Any]:
        """Analyze document tone"""
        try:
            # Simple heuristic-based tone analysis
            formal_indicators = ['therefore', 'furthermore', 'consequently', 'moreover', 'thus']
            informal_indicators = ['gonna', 'wanna', 'yeah', 'ok', 'cool']
            
            doc_lower = doc.lower()
            formal_count = sum(1 for word in formal_indicators if word in doc_lower)
            informal_count = sum(1 for word in informal_indicators if word in doc_lower)
            
            total = formal_count + informal_count
            formality_score = (formal_count / total * 100) if total > 0 else 70
            
            return {
                "tone": "formal" if formality_score > 60 else "informal",
                "formality_score": round(formality_score, 2),
                "formal_indicators": formal_count,
                "informal_indicators": informal_count,
                "assessment": "Academic tone maintained" if formality_score > 60 else "Consider more formal language"
            }
        except Exception as e:
            logger.error(f"Tone analysis error: {e}")
            return {"tone": "unknown", "formality_score": 0, "assessment": "Analysis failed"}


class CitationChecker:
    """Basic citation analysis"""
    
    def analyze(self, doc: str) -> Dict[str, Any]:
        """Analyze citations in document"""
        try:
            # Detect common citation patterns
            citation_patterns = [
                r'\([A-Z][a-z]+,?\s+\d{4}\)',  # (Author, 2020)
                r'\[[0-9]+\]',  # [1]
                r'\([A-Z][a-z]+\s+et\s+al\.,?\s+\d{4}\)',  # (Author et al., 2020)
            ]
            
            citation_count = 0
            for pattern in citation_patterns:
                citation_count += len(re.findall(pattern, doc))
            
            word_count = len(doc.split())
            citations_per_1000 = (citation_count / word_count * 1000) if word_count > 0 else 0
            
            # Assessment
            if citations_per_1000 > 10:
                assessment = "Excellent citation density"
                score = 95
            elif citations_per_1000 > 5:
                assessment = "Good citation coverage"
                score = 80
            elif citations_per_1000 > 2:
                assessment = "Adequate citations"
                score = 65
            else:
                assessment = "Consider adding more citations"
                score = 40
            
            return {
                "citation_count": citation_count,
                "citations_per_1000_words": round(citations_per_1000, 2),
                "score": score,
                "assessment": assessment
            }
        except Exception as e:
            logger.error(f"Citation analysis error: {e}")
            return {"citation_count": 0, "score": 0, "assessment": "Analysis failed"}


class ResearchIntelligenceSystem:
    """
    Industry-grade unified research intelligence system.
    Orchestrates plagiarism detection and quality analysis.
    """
    
    def __init__(self):
        """Initialize all analysis engines"""
        logger.info("Initializing Research Intelligence System")
        
        # Plagiarism engines
        self.rabin_karp = RabinKarpPlagiarism(
            window_size=settings.rabin_karp_window_size
        )
        self.tfidf_engine = TFIDFSimilarity()
        self.semantic_engine = SemanticSimilarity()
        
        # Universal Truth Filter - filters out common knowledge
        try:
            self.truth_filter = UniversalTruthFilter(model=self.semantic_engine.model)
            logger.info("Universal Truth Filter initialized - will filter common knowledge")
        except Exception as e:
            logger.warning(f"Universal Truth Filter initialization failed: {e}")
            self.truth_filter = None
        
        # Quality engines
        self.tone_checker = ToneChecker()
        self.citation_checker = CitationChecker()
        
        # Preprocessor
        self.preprocessor = TextPreprocessor()
        
        logger.info("Research Intelligence System initialized successfully")
    
    def analyze_text(
        self,
        document_text: str,
        reference_texts: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze document text for plagiarism and quality.
        
        Args:
            document_text: The document to analyze
            reference_texts: Optional reference corpus for plagiarism detection
            
        Returns:
            Complete analysis results as dictionary
        """
        try:
            logger.info("Starting text analysis")
            
            # Validation
            if not document_text or len(document_text.strip()) < 100:
                raise InsufficientDataError(
                    "Document too short for analysis (minimum 100 characters)",
                    details={"length": len(document_text)}
                )
            
            # Get text statistics
            stats = self.preprocessor.get_statistics(document_text)
            logger.info(f"Document statistics: {stats['word_count']} words, {stats['sentence_count']} sentences")
            
            # Plagiarism Analysis
            plagiarism_results = self._analyze_plagiarism(document_text, reference_texts)
            
            # Quality Analysis
            quality_results = self._analyze_quality(document_text)
            
            # Calculate final scores
            final_scores = self._calculate_final_scores(plagiarism_results, quality_results)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                plagiarism_results,
                quality_results,
                final_scores
            )
            
            result = AnalysisResult(
                plagiarism_analysis=plagiarism_results,
                quality_analysis=quality_results,
                final_scores=final_scores,
                statistics=stats,
                recommendations=recommendations
            )
            
            logger.info("Text analysis completed successfully")
            return asdict(result)
            
        except (InsufficientDataError, AnalysisError):
            raise
        except Exception as e:
            logger.error(f"Analysis error: {e}", exc_info=True)
            raise AnalysisError(
                f"Failed to analyze text: {str(e)}",
                details={"error_type": type(e).__name__}
            )
    
    def _analyze_plagiarism(
        self,
        document_text: str,
        reference_texts: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Run plagiarism detection"""
        try:
            # Use sample references if none provided
            if not reference_texts:
                reference_texts = [
                    "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
                    "Natural language processing allows computers to understand and generate human language.",
                    "Deep learning uses neural networks with multiple layers to process complex patterns."
                ]
                logger.info("Using sample reference corpus for demonstration")
            
            # Preprocess
            doc_words = self.preprocessor.preprocess_for_tokens(document_text)
            doc_sentences = self.preprocessor.preprocess_for_sentences(document_text)
            
            ref_words_list = [self.preprocessor.preprocess_for_tokens(ref) for ref in reference_texts]
            ref_sentences = [s for ref in reference_texts for s in self.preprocessor.preprocess_for_sentences(ref)]
            
            # Run engines
            results = {}
            
            # Rabin-Karp (Exact Match)
            try:
                rk_result = self.rabin_karp.calculate_similarity(doc_words, ref_words_list)
                results['exact_match'] = {
                    'score': rk_result.similarity_score,
                    'matched_count': rk_result.matched_count,
                    'total_windows': rk_result.total_windows,
                    'coverage_percentage': rk_result.coverage_percentage,
                    'sample_matches': [m.matched_text for m in rk_result.matched_windows[:3]]
                }
            except Exception as e:
                logger.warning(f"Rabin-Karp analysis failed: {e}")
                results['exact_match'] = {'score': 0.0, 'error': str(e)}
            
            # TF-IDF (Lexical Similarity)
            try:
                tfidf_result = self.tfidf_engine.calculate_similarity(document_text, reference_texts)
                results['lexical_similarity'] = {
                    'score': tfidf_result.similarity_score,
                    'max_similarity': tfidf_result.max_similarity,
                    'avg_similarity': tfidf_result.avg_similarity
                }
            except Exception as e:
                logger.warning(f"TF-IDF analysis failed: {e}")
                results['lexical_similarity'] = {'score': 0.0, 'error': str(e)}
            
            # Semantic Similarity
            try:
                semantic_result = self.semantic_engine.calculate_similarity(doc_sentences, ref_sentences)
                results['semantic_similarity'] = {
                    'score': semantic_result.similarity_score,
                    'max_similarity': semantic_result.max_similarity,
                    'sentence_count': semantic_result.sentence_count
                }
            except Exception as e:
                logger.warning(f"Semantic analysis failed: {e}")
                results['semantic_similarity'] = {'score': 0.0, 'error': str(e)}
            
            # Calculate weighted plagiarism score
            weights = settings.hybrid_weights
            overall_score = (
                weights['alpha'] * results.get('exact_match', {}).get('score', 0) +
                weights['beta'] * results.get('lexical_similarity', {}).get('score', 0) +
                weights['gamma'] * results.get('semantic_similarity', {}).get('score', 0)
            )
            
            # Apply Universal Truth Filter to remove common knowledge
            if self.truth_filter:
                try:
                    adjustment = self.truth_filter.adjust_plagiarism_score(
                        raw_score=overall_score,
                        sentences=doc_sentences,
                        threshold=0.85
                    )
                    results['truth_filter'] = adjustment
                    results['overall_plagiarism_score'] = adjustment['adjusted_score']
                    results['original_plagiarism_score'] = adjustment['original_score']
                    results['universal_truths_filtered'] = adjustment['truths_found']
                    logger.info(
                        f"Universal Truth Filter: {adjustment['truths_found']} common knowledge statements filtered. "
                        f"Score adjusted: {adjustment['original_score']:.2%} → {adjustment['adjusted_score']:.2%}"
                    )
                except Exception as e:
                    logger.warning(f"Truth filter failed: {e}")
                    results['overall_plagiarism_score'] = round(overall_score, 4)
            else:
                results['overall_plagiarism_score'] = round(overall_score, 4)
            
            results['risk_level'] = self._get_risk_level(results['overall_plagiarism_score'])
            
            return results
            
        except Exception as e:
            logger.error(f"Plagiarism analysis error: {e}", exc_info=True)
            return {'overall_plagiarism_score': 0.0, 'error': str(e)}
    
    def _analyze_quality(self, document_text: str) -> Dict[str, Any]:
        """Run quality analysis"""
        try:
            results = {}
            
            # Tone analysis
            results['tone'] = self.tone_checker.analyze(document_text)
            
            # Citation analysis
            results['citations'] = self.citation_checker.analyze(document_text)
            
            # Basic structure analysis
            paragraphs = document_text.split('\n\n')
            results['structure'] = {
                'paragraph_count': len([p for p in paragraphs if p.strip()]),
                'avg_paragraph_length': sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0,
                'assessment': 'Well-structured' if len(paragraphs) > 3 else 'Consider adding more paragraphs'
            }
            
            # Basic readability
            stats = self.preprocessor.get_statistics(document_text)
            avg_sentence_length = stats.get('avg_sentence_length', 0)
            results['readability'] = {
                'avg_sentence_length': round(avg_sentence_length, 2),
                'complexity': 'High' if avg_sentence_length > 25 else 'Medium' if avg_sentence_length > 15 else 'Low',
                'assessment': 'Good readability' if 15 <= avg_sentence_length <= 25 else 'Consider adjusting sentence length'
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Quality analysis error: {e}", exc_info=True)
            return {'error': str(e)}
    
    def _calculate_final_scores(
        self,
        plagiarism_results: Dict[str, Any],
        quality_results: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate final scores"""
        try:
            # Plagiarism score (inverted - lower is better)
            plag_score = plagiarism_results.get('overall_plagiarism_score', 0)
            originality_score = max(0, 100 - (plag_score * 100))
            
            # Quality scores
            tone_score = quality_results.get('tone', {}).get('formality_score', 70)
            citation_score = quality_results.get('citations', {}).get('score', 50)
            
            # Overall score (weighted average)
            overall_score = (
                originality_score * 0.4 +
                tone_score * 0.3 +
                citation_score * 0.3
            )
            
            return {
                'originality_score': round(originality_score, 2),
                'tone_score': round(tone_score, 2),
                'citation_score': round(citation_score, 2),
                'overall_score': round(overall_score, 2)
            }
        except Exception as e:
            logger.error(f"Score calculation error: {e}")
            return {'overall_score': 0.0}
    
    def _generate_recommendations(
        self,
        plagiarism_results: Dict[str, Any],
        quality_results: Dict[str, Any],
        final_scores: Dict[str, float]
    ) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        # Plagiarism recommendations
        plag_score = plagiarism_results.get('overall_plagiarism_score', 0)
        if plag_score > settings.plagiarism_threshold_high:
            recommendations.append("⚠️ High similarity detected. Review and rephrase matched content.")
        elif plag_score > settings.plagiarism_threshold_medium:
            recommendations.append("⚡ Moderate similarity found. Consider paraphrasing some sections.")
        
        # Tone recommendations
        tone_score = quality_results.get('tone', {}).get('formality_score', 0)
        if tone_score < 60:
            recommendations.append("📝 Use more formal academic language.")
        
        # Citation recommendations
        citation_score = quality_results.get('citations', {}).get('score', 0)
        if citation_score < 60:
            recommendations.append("📚 Add more citations to support your arguments.")
        
        # Overall recommendation
        overall = final_scores.get('overall_score', 0)
        if overall >= 80:
            recommendations.append("✅ Excellent work! Minor improvements suggested above.")
        elif overall >= 60:
            recommendations.append("👍 Good quality. Address the suggestions to improve further.")
        else:
            recommendations.append("🔧 Significant improvements needed. Focus on the areas highlighted.")
        
        return recommendations if recommendations else ["✅ Analysis complete. No major issues found."]
    
    def _get_risk_level(self, score: float) -> str:
        """Determine plagiarism risk level"""
        if score >= settings.plagiarism_threshold_high:
            return "HIGH"
        elif score >= settings.plagiarism_threshold_medium:
            return "MEDIUM"
        elif score >= settings.plagiarism_threshold_low:
            return "LOW"
        else:
            return "MINIMAL"
    
    def run_full_analysis(self, doc: str, refs: List[str]) -> Dict:
        """Legacy method for backward compatibility"""
        return self.analyze_text(doc, refs)


__all__ = ["ResearchIntelligenceSystem", "AnalysisResult"]