# guidance_engine/structure_guidance.py
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class StructureGuidance:
    """
    Provides actionable guidance for improving paper structure.
    """

    def __init__(self, min_heading_coverage: float = 0.6):
        """
        Args:
            min_heading_coverage: Minimum proportion of standard headings required (0-1)
        """
        self.min_heading_coverage = min_heading_coverage

    def generate_guidance(self, structure_analysis: Dict) -> List[str]:
        guidance = []
        try:
            coverage = structure_analysis.get("heading_coverage_percent", 0) / 100
            missing_headings = structure_analysis.get("missing_headings", [])
            total_paragraphs = structure_analysis.get("total_paragraphs", 0)

            if coverage < self.min_heading_coverage:
                guidance.append(
                    f"⚠️ Heading coverage is low ({coverage*100:.1f}%). "
                    f"Missing sections: {', '.join(missing_headings)}."
                )
            else:
                guidance.append("✅ Paper has good section coverage.")

            avg_length = structure_analysis.get("average_paragraph_length_words", 0)
            if avg_length > 150:
                guidance.append(
                    f"✍️ Average paragraph length is high ({avg_length} words). "
                    "Consider breaking into smaller paragraphs for readability."
                )
            elif avg_length < 30:
                guidance.append(
                    f"⚠️ Paragraphs are very short ({avg_length} words on average). "
                    "Consider combining for better structure."
                )

            if total_paragraphs < 5:
                guidance.append("⚠️ Paper has very few paragraphs. Consider expanding content.")

        except Exception as e:
            logging.error(f"Error generating structure guidance: {str(e)}")
            guidance.append("❌ Unable to generate structure guidance due to internal error.")

        return guidance