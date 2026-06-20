import re
from typing import Dict

class CitationChecker:
    def __init__(self):
        self.patterns = {
            "apa": r"\([A-Za-z]+,\s?\d{4}\)",
            "ieee": r"\[\d+\]",
            "doi": r"10\.\d{4,9}/[-._();()/:A-Z0-9]+"
        }

    def analyze(self, text: str) -> Dict:
        results = {name: len(re.findall(pat, text)) for name, pat in self.patterns.items()}
        # Calculate density: total citations / 1000 words
        word_count = len(text.split())
        results["density"] = float(round(sum(results.values()) / max(word_count/1000, 1), 2))
        return results
