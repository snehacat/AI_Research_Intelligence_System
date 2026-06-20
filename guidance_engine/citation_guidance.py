# guidance_engine/citation_guidance.py
import re
import logging
from typing import Dict, List, Union

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class CitationGuidance:
    """
    Provides actionable guidance for improving citation coverage in research papers.
    Works with APA, IEEE, and numeric-style citations.
    """

    def __init__(self, long_sentence_threshold: int = 40, max_missing_ratio: float = 0.2):
        """
        Args:
            long_sentence_threshold: Minimum number of words in a sentence that requires a citation
            max_missing_ratio: Maximum allowed ratio of long sentences without citations
        """
        self.long_sentence_threshold = long_sentence_threshold
        self.max_missing_ratio = max_missing_ratio

        # Patterns for common citation styles
        self.apa_pattern = r"\([A-Za-z]+,\s?\d{4}\)"
        self.ieee_pattern = r"\[\d+\]"
        self.year_only_pattern = r"\(\d{4}\)"

        self.sentence_split_pattern = r"[.!?]"

    def analyze_text(self, text: str) -> Dict[str, Union[int, float]]:
        """
        Analyze text for citation coverage.
        Returns:
            Dictionary containing total citations and long sentences missing citations
        """
        try:
            sentences = [
                s.strip()
                for s in re.split(self.sentence_split_pattern, text)
                if s.strip()
            ]
            total_sentences = len(sentences)
            long_sentences = [
                s
                for s in sentences
                if len(s.split()) >= self.long_sentence_threshold
            ]

            missing_citations = 0
            for sentence in long_sentences:
                if not re.search(self.apa_pattern, sentence) and not re.search(
                    self.ieee_pattern, sentence
                ):
                    missing_citations += 1

            apa_citations = len(re.findall(self.apa_pattern, text))
            ieee_citations = len(re.findall(self.ieee_pattern, text))
            year_mentions = len(re.findall(self.year_only_pattern, text))

            return {
                "total_sentences": total_sentences,
                "long_sentences": len(long_sentences),
                "long_sentences_missing_citations": missing_citations,
                "apa_citations": apa_citations,
                "ieee_citations": ieee_citations,
                "year_mentions": year_mentions,
                "missing_ratio": float(
                    missing_citations / max(len(long_sentences), 1)
                ),
            }

        except Exception as e:
            logging.error(f"Error analyzing citations: {str(e)}")
            return {
                "total_sentences": 0,
                "long_sentences": 0,
                "long_sentences_missing_citations": 0,
                "apa_citations": 0,
                "ieee_citations": 0,
                "year_mentions": 0,
                "missing_ratio": 0.0,
            }

    def generate_guidance(self, analysis: Dict[str, Union[int, float]]) -> List[str]:
        """
        Generate specific, actionable citation guidance based on analysis.
        """
        guidance = []
        try:
            missing_ratio = float(analysis.get("missing_ratio", 0))
            missing_count = int(analysis.get("long_sentences_missing_citations", 0))
            total_long = int(analysis.get("long_sentences", 1))
            apa_count = int(analysis.get("apa_citations", 0))
            ieee_count = int(analysis.get("ieee_citations", 0))
            total_citations = apa_count + ieee_count

            # Overall citation assessment
            if missing_ratio > 0.5:
                guidance.append(
                    f"🚨 Critical Citation Gap ({missing_ratio*100:.0f}%):\n"
                    f"   • {missing_count} of {total_long} substantive claims lack citations\n"
                    "   • Immediate action required:\n"
                    "     - Add citations for all factual claims\n"
                    "     - Reference methodology sources\n"
                    "     - Cite theoretical frameworks\n"
                    "   • Risk: May be flagged for insufficient attribution"
                )
            elif missing_ratio > 0.3:
                guidance.append(
                    f"⚠️ Insufficient Citations ({missing_ratio*100:.0f}%):\n"
                    f"   • {missing_count} claims need supporting references\n"
                    "   • Add citations for:\n"
                    "     - Statistical data and findings\n"
                    "     - Theoretical concepts\n"
                    "     - Prior research mentioned"
                )
            elif missing_ratio > 0.1:
                guidance.append(
                    f"✓ Good Citation Coverage ({missing_ratio*100:.0f}% gaps):\n"
                    f"   • Only {missing_count} statements need citations\n"
                    "   • Review: Background section, methodology sources"
                )
            else:
                guidance.append(
                    f"✅ Excellent Citation Coverage:\n"
                    f"   • {total_citations} citations found\n"
                    "   • Comprehensive source attribution\n"
                    "   • Meets academic standards"
                )

            # Citation style guidance
            if total_citations == 0:
                guidance.append(
                    "📚 No Citations Detected:\n"
                    "   • Add references using appropriate style:\n"
                    "     - APA: (Author, Year) or Author (Year)\n"
                    "     - IEEE: [1], [2], [3]\n"
                    "     - MLA: (Author Page)\n"
                    "   • Minimum 10-15 citations for research paper\n"
                    "   • Include: seminal works, recent studies, methodology sources"
                )
            elif total_citations < 5:
                guidance.append(
                    f"📖 Limited Citations ({total_citations} found):\n"
                    "   • Increase reference count to 10-15 minimum\n"
                    "   • Add citations for:\n"
                    "     - Literature review (5-8 sources)\n"
                    "     - Methodology (2-3 sources)\n"
                    "     - Discussion comparisons (3-5 sources)"
                )
            elif total_citations < 10:
                guidance.append(
                    f"✓ Adequate Citations ({total_citations} found):\n"
                    "   • Consider adding 3-5 more for comprehensive coverage\n"
                    "   • Focus on: Recent studies (last 5 years)"
                )

            # Style-specific recommendations
            if apa_count > 0 and ieee_count > 0:
                guidance.append(
                    f"⚠️ Mixed Citation Styles:\n"
                    f"   • Found both APA ({apa_count}) and IEEE ({ieee_count}) formats\n"
                    "   • Choose ONE consistent style:\n"
                    "     - APA: Social sciences, psychology, education\n"
                    "     - IEEE: Engineering, computer science, technology\n"
                    "   • Convert all citations to chosen format"
                )
            elif apa_count > 0:
                guidance.append(
                    f"✓ Using APA Style ({apa_count} citations):\n"
                    "   • Ensure consistency: (Author, Year) format\n"
                    "   • Include page numbers for direct quotes\n"
                    "   • Verify all citations in reference list"
                )
            elif ieee_count > 0:
                guidance.append(
                    f"✓ Using IEEE Style ({ieee_count} citations):\n"
                    "   • Ensure sequential numbering [1], [2], [3]\n"
                    "   • Place citations before punctuation\n"
                    "   • Verify all numbers in reference list"
                )

            # Specific improvement actions
            if missing_count > 0:
                guidance.append(
                    f"🎯 Action Items for {missing_count} Uncited Claims:\n"
                    "   1. Identify factual statements without sources\n"
                    "   2. Search Google Scholar for supporting literature\n"
                    "   3. Add in-text citations immediately after claims\n"
                    "   4. Update reference list with full citations\n"
                    "   5. Verify citation format consistency"
                )

            # Quality indicators
            if total_citations >= 15 and missing_ratio < 0.1:
                guidance.append(
                    "🌟 Publication-Ready Citations:\n"
                    "   • Comprehensive source coverage\n"
                    "   • Proper attribution throughout\n"
                    "   • Meets journal standards"
                )

        except Exception as e:
            logging.error(f"Error generating citation guidance: {str(e)}")
            guidance.append(
                "❌ Unable to generate citation guidance. Please check your document."
            )

        return guidance
