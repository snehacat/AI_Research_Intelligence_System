# guidance_engine/improvement_path.py
import logging
from typing import Dict, List

from guidance_engine.citation_guidance import CitationGuidance
from guidance_engine.plagiarism_guidance import PlagiarismGuidance
from guidance_engine.structure_guidance import StructureGuidance
from guidance_engine.tone_guidance import ToneGuidance

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class ImprovementPathGenerator:
    """
    Generates a professional, actionable improvement plan for research papers
    based on plagiarism, tone, citations, structure, and readability.
    """

    def __init__(self):
        self.plagiarism_guidance = PlagiarismGuidance()
        self.citation_guidance = CitationGuidance()
        self.structure_guidance = StructureGuidance()
        self.tone_guidance = ToneGuidance()

    def generate_plan(
        self,
        plagiarism_data: Dict,
        tone_data: Dict,
        citation_data: Dict,
        structure_data: Dict,
        readability_data: Dict,
        final_score: float
    ) -> List[str]:
        """
        Generate comprehensive, context-aware improvement plan.
        """

        improvement_plan = []

        try:
            # Overall score assessment
            if final_score >= 85:
                improvement_plan.append(
                    f"🎉 EXCELLENT WORK (Score: {final_score:.0f}/100):\n"
                    "   • Your paper meets high academic standards\n"
                    "   • Ready for submission with minor refinements\n"
                    "   • Strong potential for publication"
                )
            elif final_score >= 70:
                improvement_plan.append(
                    f"✓ GOOD QUALITY (Score: {final_score:.0f}/100):\n"
                    "   • Solid foundation with room for improvement\n"
                    "   • Address key issues below before submission\n"
                    "   • Expected revision time: 2-4 hours"
                )
            elif final_score >= 50:
                improvement_plan.append(
                    f"⚠️ NEEDS IMPROVEMENT (Score: {final_score:.0f}/100):\n"
                    "   • Significant revisions required\n"
                    "   • Focus on priority issues first\n"
                    "   • Expected revision time: 1-2 days"
                )
            else:
                improvement_plan.append(
                    f"🚨 MAJOR REVISION NEEDED (Score: {final_score:.0f}/100):\n"
                    "   • Substantial work required across multiple areas\n"
                    "   • Consider restructuring approach\n"
                    "   • Expected revision time: 3-5 days"
                )

            improvement_plan.append("\n" + "="*60 + "\n")

            # Priority-based guidance
            improvement_plan.append("📋 PRIORITY IMPROVEMENTS:\n")

            # --- Plagiarism Guidance (Highest Priority) ---
            plagiarism_steps = self.plagiarism_guidance.generate_guidance(plagiarism_data)
            if plagiarism_steps:
                improvement_plan.append("\n🔴 PRIORITY 1: Originality & Plagiarism")
                improvement_plan.extend(plagiarism_steps)

            # --- Citation Guidance (High Priority) ---
            citation_steps = self.citation_guidance.generate_guidance(citation_data)
            if citation_steps:
                improvement_plan.append("\n🟠 PRIORITY 2: Citations & References")
                improvement_plan.extend(citation_steps)

            # --- Tone Guidance (Medium Priority) ---
            total_sentences = readability_data.get("sentences", 1)
            tone_steps = self.tone_guidance.generate_guidance(tone_data, total_sentences)
            if tone_steps:
                improvement_plan.append("\n🟡 PRIORITY 3: Academic Tone & Style")
                improvement_plan.extend(tone_steps)

            # --- Structure Guidance ---
            structure_steps = self.structure_guidance.generate_guidance(structure_data)
            if structure_steps:
                improvement_plan.append("\n🟢 PRIORITY 4: Structure & Organization")
                improvement_plan.extend(structure_steps)

            # --- Readability Guidance ---
            readability_score = readability_data.get("flesch_reading_ease", 0)
            avg_sentence_length = readability_data.get("avg_sentence_length", 0)
            complex_words = readability_data.get("complex_word_count", 0)
            
            improvement_plan.append("\n🔵 PRIORITY 5: Readability & Clarity")
            
            if readability_score < 30:
                improvement_plan.append(
                    f"⚠️ Very Difficult to Read (Score: {readability_score:.0f}):\n"
                    f"   • Average sentence length: {avg_sentence_length:.1f} words\n"
                    "   • Actions:\n"
                    "     - Break long sentences (aim for 15-20 words)\n"
                    "     - Simplify complex terminology where possible\n"
                    "     - Add transition words for flow\n"
                    "     - Use active voice more frequently"
                )
            elif readability_score < 50:
                improvement_plan.append(
                    f"✓ Difficult (Score: {readability_score:.0f}):\n"
                    "   • Appropriate for academic audience\n"
                    "   • Consider simplifying 2-3 complex paragraphs\n"
                    "   • Add subheadings for better navigation"
                )
            elif readability_score < 60:
                improvement_plan.append(
                    f"✅ Standard Academic Level (Score: {readability_score:.0f}):\n"
                    "   • Well-balanced complexity\n"
                    "   • Suitable for journal publication\n"
                    "   • Maintain current writing style"
                )
            else:
                improvement_plan.append(
                    f"✅ Highly Readable (Score: {readability_score:.0f}):\n"
                    "   • Clear and accessible writing\n"
                    "   • Excellent for broad academic audience"
                )

            # Final action checklist
            improvement_plan.append("\n" + "="*60)
            improvement_plan.append("\n✅ FINAL CHECKLIST BEFORE SUBMISSION:\n")
            improvement_plan.append("   □ All similarity issues addressed")
            improvement_plan.append("   □ Citations added for all claims")
            improvement_plan.append("   □ Informal language replaced")
            improvement_plan.append("   □ Consistent citation style used")
            improvement_plan.append("   □ Abstract summarizes key findings")
            improvement_plan.append("   □ Conclusion restates contributions")
            improvement_plan.append("   □ References formatted correctly")
            improvement_plan.append("   □ Proofread for grammar and spelling")
            improvement_plan.append("   □ Figures and tables properly labeled")
            improvement_plan.append("   □ Acknowledgments section complete")

            # Estimated revision time
            if final_score < 50:
                improvement_plan.append("\n⏱️ Estimated Revision Time: 3-5 days")
            elif final_score < 70:
                improvement_plan.append("\n⏱️ Estimated Revision Time: 1-2 days")
            elif final_score < 85:
                improvement_plan.append("\n⏱️ Estimated Revision Time: 2-4 hours")
            else:
                improvement_plan.append("\n⏱️ Estimated Revision Time: 30-60 minutes")

        except Exception as e:
            logging.error(f"Error generating improvement plan: {str(e)}")
            improvement_plan.append("❌ Unable to generate full improvement plan. Please check your document.")

        return improvement_plan
# guidance_engine/improvement_path.py
def generate_improvement_plan(*args, **kwargs):
    return ImprovementPathGenerator().generate_plan(*args, **kwargs)