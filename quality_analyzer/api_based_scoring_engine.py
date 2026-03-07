"""
quality_analyzer/api_based_scoring_engine.py
Industry-Grade API-Based Research Intelligence System
Integrates multiple APIs and local engines for robust research analysis
"""

import logging
import os
import sys
from typing import List, Dict, Any
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# API clients
from api_integrations.crossref_client import CrossRefClient
from api_integrations.semantic_scholar_client import SemanticScholarClient
from api_integrations.arxiv_client import ArxivClient
from api_integrations.openai_client import OpenAIClient
from api_integrations.language_tool_client import LanguageToolClient
from api_integrations.wikipedia_client import WikipediaClient

# Local plagiarism engines
from plagiarism_engine.rabin_karp import RabinKarpPlagiarism
from plagiarism_engine.tfidf_engine import TFIDFSimilarity
from plagiarism_engine.semantic_engine import SemanticSimilarity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)

class APIBasedResearchIntelligenceSystem:
    """
    Robust API-Based Research Intelligence System
    Combines local and API-based analyses for industrial research projects
    """

    def __init__(self, openai_api_key: str = None,
                 section_weights: Dict[str, float] = None,
                 hybrid_weights: Dict[str, float] = None):
        # Initialize API clients
        self.crossref = CrossRefClient()
        self.semantic_scholar = SemanticScholarClient()
        self.arxiv = ArxivClient()
        self.openai = OpenAIClient(openai_api_key)
        self.language_tool = LanguageToolClient()
        self.wikipedia = WikipediaClient()

        # Local engines
        self.rabin_karp = RabinKarpPlagiarism(window_size=5)
        self.tfidf_engine = TFIDFSimilarity()
        self.semantic_engine = SemanticSimilarity()

        # Section weights
        default_weights = {
            'abstract': 0.8, 'introduction': 1.0, 'literature_review': 1.2,
            'methodology': 1.0, 'results': 1.1, 'discussion': 1.0,
            'conclusion': 0.9, 'references': 0.5, 'default': 1.0
        }
        self.section_weights = section_weights or default_weights

        # Hybrid weights
        default_hybrid = {'alpha': 0.3, 'beta': 0.2, 'gamma': 0.2, 'delta': 0.3}
        hybrid = hybrid_weights or default_hybrid
        self.alpha = hybrid['alpha']
        self.beta = hybrid['beta']
        self.gamma = hybrid['gamma']
        self.delta = hybrid['delta']

        logging.info("API-Based Research Intelligence System initialized")

    # ===================== Public Method =====================
    def comprehensive_analysis(
        self,
        document: str,
        search_references: bool = True,
        enable_openai: bool = True
    ) -> Dict[str, Any]:
        """
        Main method to analyze a research document.
        Combines local plagiarism, API calls, citations, quality, and recommendations.
        """
        try:
            report = {
                'document_metadata': self._extract_document_metadata(document),
                'plagiarism_analysis': {},
                'citation_analysis': {},
                'quality_analysis': {},
                'api_analysis': {},
                'reference_papers': {},
                'recommendations': [],
                'confidence_scores': {}
            }

            # --- Step 1: Reference Search ---
            reference_papers = {}
            if search_references:
                key_terms = self._extract_key_terms(document)
                reference_papers = self._search_reference_papers(key_terms)
                report['reference_papers'] = reference_papers

            # --- Step 2: Local plagiarism analysis ---
            report['plagiarism_analysis']['local_analysis'] = self._local_plagiarism_analysis(
                document, reference_papers
            )

            # --- Step 3: API-based analysis ---
            report['api_analysis'] = self._api_based_analysis(
                document, reference_papers, enable_openai
            )

            # --- Step 4: Citation analysis ---
            report['citation_analysis'] = self._analyze_citations(document)

            # --- Step 5: Quality analysis ---
            report['quality_analysis'] = self._analyze_quality(document, enable_openai)

            # --- Step 6: Common knowledge analysis ---
            report['common_knowledge_analysis'] = self.wikipedia.check_common_knowledge(document)

            # --- Step 7: Final Scores ---
            report['final_scores'] = self._calculate_final_scores(report)

            # --- Step 8: Recommendations ---
            report['recommendations'] = self._generate_comprehensive_recommendations(report)

            # --- Step 9: Confidence Scores ---
            report['confidence_scores'] = self._calculate_confidence_scores(report)

            return report

        except Exception as e:
            logging.exception("Comprehensive analysis failed")
            return {'error': str(e), 'document_length': len(document)}

    # ===================== Private Methods =====================
    def _extract_document_metadata(self, document: str) -> Dict[str, Any]:
        sentences = [s.strip() for s in document.split('.') if s.strip()]
        words = document.split()
        return {
            'character_count': len(document),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_sentence_length': len(words) / max(len(sentences), 1),
            'estimated_reading_time_minutes': round(len(words) / 200, 2)
        }

    def _extract_key_terms(self, document: str, max_terms: int = 10) -> List[str]:
        """Extract key terms robustly using spaCy, fallback to frequency method"""
        try:
            import spacy
            from collections import Counter
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(document)
            key_terms = [token.text.lower() for token in doc
                         if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 3]
            return [term for term, _ in Counter(key_terms).most_common(max_terms)]
        except Exception as e:
            logging.warning(f"spaCy failed, using fallback: {e}")
            from collections import Counter
            stop_words = set([
                'the','a','an','and','or','but','in','on','at','to','for','of','with','by',
                'is','are','was','were','be','been','have','has','had','do','does','did','will',
                'would','could','should','may','might','can','this','that','these','those','i','you',
                'he','she','it','we','they'
            ])
            words = [w for w in document.lower().split() if len(w) > 3 and w not in stop_words]
            return [term for term, _ in Counter(words).most_common(max_terms)]

    def _search_reference_papers(self, key_terms: List[str]) -> Dict[str, List]:
        references = {'crossref': [], 'semantic_scholar': [], 'arxiv': []}
        try:
            # Search arXiv first (most reliable)
            for term in key_terms[:3]:
                try:
                    arxiv_papers = self.arxiv.search_papers(term, max_results=2)
                    references['arxiv'].extend(arxiv_papers)
                    if arxiv_papers:
                        logging.info(f"Found {len(arxiv_papers)} arXiv papers for term: {term}")
                except Exception as e:
                    logging.warning(f"arXiv search failed for term '{term}': {e}")
            
            # Search Semantic Scholar with rate limiting
            import time
            for i, term in enumerate(key_terms[:2]):
                try:
                    if i > 0:  # Add delay between requests
                        time.sleep(1)
                    ss_papers = self.semantic_scholar.search_papers(term, limit=2)
                    references['semantic_scholar'].extend(ss_papers)
                    if ss_papers:
                        logging.info(f"Found {len(ss_papers)} Semantic Scholar papers for term: {term}")
                except Exception as e:
                    logging.warning(f"Semantic Scholar search failed for term '{term}': {e}")
            
            # Search CrossRef as backup
            for term in key_terms[:2]:
                try:
                    crossref_papers = self.crossref.search_references(term, limit=2)
                    references['crossref'].extend(crossref_papers)
                    if crossref_papers:
                        logging.info(f"Found {len(crossref_papers)} CrossRef papers for term: {term}")
                except Exception as e:
                    logging.warning(f"CrossRef search failed for term '{term}': {e}")
                    
        except Exception as e:
            logging.error(f"Reference search failed: {e}")
        
        # Log total results
        total_refs = sum(len(papers) for papers in references.values())
        logging.info(f"Total reference papers found: {total_refs}")
        
        return references

    def _local_plagiarism_analysis(self, document: str, reference_papers: Dict[str, List]) -> Dict[str, Any]:
        reference_texts = []
        for source in reference_papers.values():
            for paper in source:
                reference_texts.append(paper.get('abstract') or paper.get('summary') or paper.get('title'))

        # Handle Rabin-Karp similarity
        ems, matched_windows = self.rabin_karp.calculate_similarity(document.split(), [ref.split() for ref in reference_texts])
        
        # Handle TF-IDF similarity
        lss_result = self.tfidf_engine.calculate_similarity(document, reference_texts)
        lss = lss_result.get('score', 0.0) if isinstance(lss_result, dict) else lss_result
        
        # Handle Semantic similarity
        sss = self.semantic_engine.calculate_similarity([document], reference_texts)
        
        combined = round(self.alpha*ems + self.beta*lss + self.gamma*sss, 4)

        return {
            'exact_match_score': round(ems, 4),
            'lexical_similarity_score': round(lss, 4),
            'semantic_similarity_score': round(sss, 4),
            'combined_local_score': combined,
            'matched_windows': matched_windows,
            'reference_count': len(reference_texts)
        }

    def _api_based_analysis(self, document: str, reference_papers: Dict[str, List], enable_openai: bool) -> Dict[str, Any]:
        api_results = {}
        try:
            if enable_openai and self.openai.is_configured():
                api_results['openai'] = {
                    'paraphrasing_suggestions': self.openai.paraphrase_text(document[:500]),
                    'writing_improvement': self.openai.improve_academic_writing(document[:1000]),
                    'plagiarism_risk': self.openai.check_plagiarism_risk(document[:1000])
                }
            else:
                api_results['openai'] = {'status': 'disabled'}

            api_results['grammar_check'] = self.language_tool.get_academic_style_suggestions(document)
            api_results['wikipedia_analysis'] = self.wikipedia.check_common_knowledge(document)
        except Exception as e:
            logging.error(f"API analysis failed: {e}")
            api_results['error'] = str(e)
        return api_results

    def _analyze_citations(self, document: str) -> Dict[str, Any]:
        """Analyze citation patterns and quality"""
        try:
            import re
            # Find citation patterns
            citation_patterns = [
                r'\[(\d+(?:,\s*\d+)*)\]',  # [1], [1,2,3]
                r'\([A-Za-z]+,\s*\d{4}\)',  # (Smith, 2020)
                r'[A-Za-z]+\s+et\s+al\.?\s*\(\d{4}\)',  # Smith et al. (2020)
            ]
            
            total_citations = 0
            citation_types = {'numeric': 0, 'author_year': 0, 'et_al': 0}
            
            for pattern in citation_patterns:
                matches = re.findall(pattern, document)
                total_citations += len(matches)
                if pattern == citation_patterns[0]:
                    citation_types['numeric'] += len(matches)
                elif pattern == citation_patterns[1]:
                    citation_types['author_year'] += len(matches)
                else:
                    citation_types['et_al'] += len(matches)
            
            # Calculate citation density
            word_count = len(document.split())
            citation_density = total_citations / max(word_count, 1) * 1000
            
            return {
                'total_citations': total_citations,
                'citation_density_per_1000_words': round(citation_density, 2),
                'citation_types': citation_types,
                'citation_score': min(100, total_citations * 2),  # Simple scoring
                'recommendations': self._generate_citation_recommendations(total_citations, word_count)
            }
        except Exception as e:
            logging.error(f"Citation analysis failed: {e}")
            return {'error': str(e), 'total_citations': 0}
    
    def _generate_citation_recommendations(self, citations: int, word_count: int) -> List[str]:
        """Generate citation-specific recommendations"""
        recommendations = []
        density = citations / max(word_count, 1) * 1000
        
        if citations == 0:
            recommendations.append("No citations found. Add references to support your claims.")
        elif citations < 3:
            recommendations.append("Very few citations. Consider adding more references to strengthen your argument.")
        elif density < 5:
            recommendations.append("Low citation density. Add more references throughout your document.")
        elif density > 50:
            recommendations.append("Very high citation density. Ensure you're providing enough original analysis.")
        else:
            recommendations.append("Citation density appears appropriate for academic writing.")
            
        return recommendations

    def _analyze_quality(self, document: str, enable_openai: bool = False) -> Dict[str, Any]:
        """Analyze document quality metrics"""
        try:
            # Basic readability metrics
            sentences = [s.strip() for s in document.split('.') if s.strip()]
            words = document.split()
            
            avg_sentence_length = len(words) / max(len(sentences), 1)
            complex_words = [w for w in words if len(w) > 6]
            complex_word_ratio = len(complex_words) / max(len(words), 1)
            
            # Academic tone indicators
            academic_phrases = [
                'furthermore', 'however', 'therefore', 'consequently', 'moreover',
                'in addition', 'on the other hand', 'in contrast', 'similarly'
            ]
            academic_phrase_count = sum(1 for phrase in academic_phrases if phrase in document.lower())
            
            # Structure analysis
            sections = ['abstract', 'introduction', 'methodology', 'results', 'discussion', 'conclusion']
            found_sections = [s for s in sections if s in document.lower()]
            
            quality_score = min(100, (
                (20 if 10 <= avg_sentence_length <= 20 else 10) +
                (20 if complex_word_ratio >= 0.1 else 10) +
                (20 if academic_phrase_count >= 3 else 10) +
                (40 if len(found_sections) >= 4 else 20)
            ))
            
            return {
                'readability_score': quality_score,
                'avg_sentence_length': round(avg_sentence_length, 1),
                'complex_word_ratio': round(complex_word_ratio, 3),
                'academic_phrase_count': academic_phrase_count,
                'structure_sections': found_sections,
                'total_sections_found': len(found_sections),
                'quality_recommendations': self._generate_quality_recommendations(
                    avg_sentence_length, complex_word_ratio, academic_phrase_count, found_sections
                )
            }
        except Exception as e:
            logging.error(f"Quality analysis failed: {e}")
            return {'error': str(e), 'quality_score': 0}
    
    def _generate_quality_recommendations(self, avg_sent_len: float, complex_ratio: float, 
                                        academic_count: int, sections: List[str]) -> List[str]:
        """Generate quality improvement recommendations"""
        recommendations = []
        
        if avg_sent_len < 10:
            recommendations.append("Sentences are too short. Use more complex sentence structures for academic writing.")
        elif avg_sent_len > 25:
            recommendations.append("Sentences are very long. Consider breaking down complex sentences.")
        
        if complex_ratio < 0.1:
            recommendations.append("Low vocabulary complexity. Use more precise and technical terminology.")
        
        if academic_count < 3:
            recommendations.append("Add more transition words and phrases to improve academic flow.")
        
        if len(sections) < 4:
            recommendations.append("Ensure your paper has clear sections (introduction, methodology, results, discussion, conclusion).")
        
        if not recommendations:
            recommendations.append("Document structure and readability appear good for academic writing.")
            
        return recommendations

    def _calculate_final_scores(self, report: Dict[str, Any]) -> Dict[str, float]:
        """Calculate comprehensive final scores"""
        try:
            # Get component scores
            plagiarism_score = report.get('plagiarism_analysis', {}).get('local_analysis', {}).get('combined_local_score', 0)
            citation_score = report.get('citation_analysis', {}).get('citation_score', 0)
            quality_score = report.get('quality_analysis', {}).get('readability_score', 0)
            
            # Calculate originality (inverse of plagiarism)
            originality_score = max(0, 100 - plagiarism_score * 100)
            
            # Weighted overall score
            overall_score = (
                self.delta * originality_score +  # Originality weight
                self.alpha * quality_score +      # Quality weight  
                self.beta * citation_score        # Citation weight
            )
            
            return {
                'overall_score': round(min(100, overall_score), 1),
                'originality_score': round(originality_score, 1),
                'plagiarism_score': round(plagiarism_score, 4),
                'quality_score': round(quality_score, 1),
                'citation_score': round(citation_score, 1)
            }
        except Exception as e:
            logging.error(f"Score calculation failed: {e}")
            return {
                'overall_score': 0, 'originality_score': 0, 'plagiarism_score': 0,
                'quality_score': 0, 'citation_score': 0
            }
    
    def _generate_comprehensive_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate overall recommendations"""
        recommendations = []
        
        # Add citation recommendations
        citation_recs = report.get('citation_analysis', {}).get('recommendations', [])
        recommendations.extend(citation_recs)
        
        # Add quality recommendations  
        quality_recs = report.get('quality_analysis', {}).get('quality_recommendations', [])
        recommendations.extend(quality_recs)
        
        # Add API-based recommendations if available
        api_results = report.get('api_analysis', {})
        if 'grammar_check' in api_results and isinstance(api_results['grammar_check'], list):
            recommendations.extend(api_results['grammar_check'][:3])
        
        # Ensure we have recommendations
        if not recommendations:
            recommendations.append("Document appears to be well-structured. Continue with current approach.")
            
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def _calculate_confidence_scores(self, report: Dict[str, Any]) -> Dict[str, float]:
        """Calculate confidence scores for different analysis components"""
        try:
            # Base confidence on data availability
            reference_count = report.get('plagiarism_analysis', {}).get('local_analysis', {}).get('reference_count', 0)
            api_success = not any('error' in str(v) for v in report.get('api_analysis', {}).values() if isinstance(v, dict))
            
            confidence_scores = {
                'plagiarism_confidence': min(100, reference_count * 10 + 50),
                'citation_confidence': 85,  # High confidence in citation analysis
                'quality_confidence': 90,   # High confidence in quality metrics
                'overall_confidence': 75    # Moderate overall confidence
            }
            
            # Adjust based on API success
            if api_success:
                confidence_scores['overall_confidence'] += 10
                
            return {k: round(v, 1) for k, v in confidence_scores.items()}
        except Exception as e:
            logging.error(f"Confidence calculation failed: {e}")
            return {'overall_confidence': 50}
