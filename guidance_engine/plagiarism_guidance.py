# guidance_engine/plagiarism_guidance.py
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class PlagiarismGuidance:
    """
    Provides actionable, context-aware guidance for improving originality in research papers.
    """

    def __init__(self, threshold: float = 20.0):
        self.threshold = threshold

    def generate_guidance(self, plagiarism_data: Dict) -> List[str]:
        """
        Generate specific, actionable plagiarism improvement guidance.
        """
        guidance = []

        try:
            overall = plagiarism_data.get("overall_plagiarism_score", 0) * 100
            risk_level = plagiarism_data.get("risk_level", "UNKNOWN")
            rabin = plagiarism_data.get("rabin_karp_score", 0) * 100
            tfidf = plagiarism_data.get("tfidf_score", 0) * 100
            semantic = plagiarism_data.get("semantic_score", 0) * 100
            
            # Get matched sections if available
            matched_sections = plagiarism_data.get("matched_sections", [])
            high_similarity_sentences = plagiarism_data.get("high_similarity_sentences", [])

            # Risk-based guidance
            if risk_level == "HIGH":
                guidance.append(
                    f"🚨 HIGH RISK: {overall:.1f}% similarity detected. Immediate action required:\n"
                    "   • Paraphrase all similar sections using your own words\n"
                    "   • Add proper citations for all referenced ideas\n"
                    "   • Rewrite methodology and results in original language"
                )
            elif risk_level == "MEDIUM":
                guidance.append(
                    f"⚠️ MEDIUM RISK: {overall:.1f}% similarity. Recommended improvements:\n"
                    "   • Review and rephrase sections with high similarity\n"
                    "   • Ensure all quotes are properly attributed\n"
                    "   • Add more original analysis and interpretation"
                )
            elif risk_level == "LOW":
                guidance.append(
                    f"✓ LOW RISK: {overall:.1f}% similarity. Minor improvements:\n"
                    "   • Double-check citation formatting\n"
                    "   • Ensure paraphrasing is sufficiently different from sources"
                )
            else:
                guidance.append(
                    f"✅ MINIMAL RISK: {overall:.1f}% similarity. Excellent originality!\n"
                    "   • Maintain current writing standards\n"
                    "   • Continue using proper citations"
                )

            # Engine-specific actionable guidance
            if rabin > 25:
                guidance.append(
                    f"🔍 Exact Match Detection ({rabin:.1f}%):\n"
                    "   • Found word-for-word matches with reference texts\n"
                    "   • Action: Use quotation marks for direct quotes\n"
                    "   • Action: Paraphrase common phrases and terminology\n"
                    "   • Action: Replace copied sentences with original explanations"
                )
            
            if tfidf > 30:
                guidance.append(
                    f"📊 Lexical Similarity ({tfidf:.1f}%):\n"
                    "   • Similar vocabulary and phrasing patterns detected\n"
                    "   • Action: Use synonyms and alternative expressions\n"
                    "   • Action: Restructure sentence patterns\n"
                    "   • Action: Add your own examples and explanations"
                )
            
            if semantic > 40:
                guidance.append(
                    f"🧠 Semantic Similarity ({semantic:.1f}%):\n"
                    "   • Ideas and concepts closely match existing work\n"
                    "   • Action: Add unique insights and perspectives\n"
                    "   • Action: Provide original analysis of findings\n"
                    "   • Action: Cite sources when building on others' ideas"
                )

            # Specific section guidance
            if matched_sections:
                guidance.append(
                    f"📍 High-Similarity Sections Found:\n"
                    f"   • {len(matched_sections)} section(s) need attention\n"
                    "   • Focus on: Introduction, Literature Review, Methodology\n"
                    "   • Rewrite these sections with original language"
                )

            # Positive reinforcement
            if overall < 15:
                guidance.append(
                    "🌟 Strong Originality:\n"
                    "   • Your work shows excellent original thinking\n"
                    "   • Continue developing unique perspectives\n"
                    "   • Consider publishing this original research"
                )

        except Exception as e:
            logging.error(f"Error generating plagiarism guidance: {str(e)}")
            guidance.append("❌ Unable to generate plagiarism guidance. Please check your document.")

        return guidance