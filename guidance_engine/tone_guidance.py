# guidance_engine/tone_guidance.py
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class ToneGuidance:
    """
    Provides specific, actionable guidance to improve writing tone and academic style.
    """

    def __init__(self, passive_threshold: float = 0.3, informal_threshold: int = 3):
        self.passive_threshold = passive_threshold
        self.informal_threshold = informal_threshold

    def generate_guidance(self, tone_analysis: Dict[str, int], total_sentences: int = 1) -> List[str]:
        """
        Generate context-aware tone improvement guidance.
        """
        guidance = []
        try:
            passive_count = tone_analysis.get("passive_voice_estimate", 0)
            passive_ratio = passive_count / max(total_sentences, 1)
            informal_count = tone_analysis.get("informal_words", 0)
            first_person_count = tone_analysis.get("first_person_usage", 0)
            contractions_count = tone_analysis.get("contractions", 0)
            
            # Calculate tone score
            tone_issues = 0
            if passive_ratio > self.passive_threshold:
                tone_issues += 1
            if informal_count > self.informal_threshold:
                tone_issues += 1
            if first_person_count > 5:
                tone_issues += 1
            if contractions_count > 0:
                tone_issues += 1

            # Overall tone assessment
            if tone_issues == 0:
                guidance.append(
                    "✅ Excellent Academic Tone:\n"
                    "   • Formal language maintained throughout\n"
                    "   • Appropriate voice and style\n"
                    "   • Professional presentation"
                )
            elif tone_issues <= 2:
                guidance.append(
                    "✓ Good Tone with Minor Issues:\n"
                    "   • Overall professional writing\n"
                    "   • Few areas need refinement"
                )
            else:
                guidance.append(
                    "⚠️ Tone Needs Improvement:\n"
                    "   • Multiple informal elements detected\n"
                    "   • Requires significant revision for academic standards"
                )

            # Specific, actionable guidance
            if passive_ratio > self.passive_threshold:
                active_needed = int(passive_count * 0.6)  # Aim to convert 60% to active
                guidance.append(
                    f"📝 Passive Voice ({passive_count} instances, {passive_ratio*100:.1f}%):\n"
                    f"   • Convert ~{active_needed} sentences to active voice\n"
                    "   • Example: 'The experiment was conducted' → 'We conducted the experiment'\n"
                    "   • Example: 'Results were analyzed' → 'The study analyzed results'\n"
                    "   • Focus on: Methods and Results sections"
                )
            else:
                guidance.append(
                    f"✅ Voice Balance Good ({passive_ratio*100:.1f}% passive)\n"
                    "   • Appropriate mix of active and passive voice"
                )

            if informal_count > self.informal_threshold:
                guidance.append(
                    f"🎯 Informal Language ({informal_count} words detected):\n"
                    "   • Replace casual words with academic alternatives:\n"
                    "     - 'a lot of' → 'numerous', 'substantial'\n"
                    "     - 'get' → 'obtain', 'acquire', 'achieve'\n"
                    "     - 'show' → 'demonstrate', 'indicate', 'reveal'\n"
                    "     - 'big' → 'significant', 'substantial', 'considerable'\n"
                    "     - 'thing' → 'factor', 'element', 'aspect'\n"
                    "   • Use discipline-specific terminology"
                )

            if first_person_count > 5:
                guidance.append(
                    f"👤 First-Person Usage ({first_person_count} instances):\n"
                    "   • Reduce personal pronouns in academic writing\n"
                    "   • Alternatives:\n"
                    "     - 'I believe' → 'The evidence suggests'\n"
                    "     - 'We found' → 'The analysis revealed'\n"
                    "     - 'I think' → 'It appears that', 'The data indicates'\n"
                    "   • Exception: Acceptable in methodology for clarity"
                )
            elif first_person_count > 0:
                guidance.append(
                    f"✓ Limited First-Person Use ({first_person_count} instances)\n"
                    "   • Acceptable level for academic writing\n"
                    "   • Consider reducing further for more formal tone"
                )

            if contractions_count > 0:
                guidance.append(
                    f"📖 Contractions Found ({contractions_count}):\n"
                    "   • Expand all contractions:\n"
                    "     - don't → do not\n"
                    "     - can't → cannot\n"
                    "     - won't → will not\n"
                    "     - it's → it is\n"
                    "   • Contractions are never appropriate in formal academic writing"
                )

            # Positive reinforcement
            if tone_issues == 0:
                guidance.append(
                    "🌟 Professional Writing Quality:\n"
                    "   • Maintains consistent academic tone\n"
                    "   • Suitable for publication\n"
                    "   • Demonstrates strong writing skills"
                )

        except Exception as e:
            logging.error(f"Error generating tone guidance: {str(e)}")
            guidance.append("❌ Unable to generate tone guidance. Please check your document.")

        return guidance