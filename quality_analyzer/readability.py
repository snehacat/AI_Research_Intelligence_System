import re
import logging
from typing import Dict, Optional, Any

try:
    import spacy

    nlp: Optional[Any] = spacy.load("en_core_web_sm")
except Exception:
    logging.warning(
        "spaCy model not found. Install with 'python -m spacy download en_core_web_sm'"
    )
    nlp = None

try:
    import pyphen

    dic = pyphen.Pyphen(lang="en")
except Exception:
    logging.warning("pyphen not found. Install with 'pip install pyphen'")
    dic = None


class ReadabilityAnalyzer:
    def count_syllables(self, word: str) -> int:
        word = word.lower()
        if dic:
            syllables = dic.inserted(word).split("-")
            return max(len(syllables), 1)
        else:
            # fallback simple heuristic
            vowels = "aeiouy"
            count = 0
            if word and word[0] in vowels:
                count += 1
            for i in range(1, len(word)):
                if word[i] in vowels and word[i - 1] not in vowels:
                    count += 1
            if word.endswith("e"):
                count -= 1
            return max(count, 1)

    def analyze(self, text: str) -> Dict[str, Any]:
        try:
            if nlp:
                doc = nlp(text)
                sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
            else:
                sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]

            words = re.findall(r"\b\w+\b", text)
            sentence_count = len(sentences)
            word_count = len(words)

            if sentence_count == 0 or word_count == 0:
                return {}

            syllable_count = sum(self.count_syllables(word) for word in words)
            ASL = word_count / sentence_count
            ASW = syllable_count / word_count

            # Flesch Reading Ease
            FRE = 206.835 - (1.015 * ASL) - (84.6 * ASW)
            # Flesch-Kincaid Grade Level
            FKGL = (0.39 * ASL) + (11.8 * ASW) - 15.59
            # Gunning Fog Index
            complex_words = [w for w in words if self.count_syllables(w) >= 3]
            GFI = 0.4 * (ASL + 100 * len(complex_words) / word_count)
            # SMOG Index
            SMOG = (
                1.043 * (30 * len(complex_words) / max(sentence_count, 1)) ** 0.5
                + 3.1291
            )

            return {
                "sentences": sentence_count,
                "words": word_count,
                "avg_sentence_length": round(ASL, 2),
                "syllable_count": syllable_count,
                "flesch_reading_ease": round(FRE, 2),
                "flesch_kincaid_grade": round(FKGL, 2),
                "gunning_fog_index": round(GFI, 2),
                "smog_index": round(SMOG, 2),
            }
        except Exception as e:
            logging.error(f"Readability analysis failed: {str(e)}")
            return {"error": str(e)}
