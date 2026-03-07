import re
from typing import Dict

class ToneChecker:
    def __init__(self):
        self.forbidden = ["gonna", "wanna", "stuff", "kinda", "lot"]
        self.passive_pattern = re.compile(r"\b(is|are|was|were|be|been)\s+\w+ed\b", re.I)

    def analyze(self, text: str) -> Dict:
        passive = len(self.passive_pattern.findall(text))
        informal = sum(len(re.findall(rf"\b{w}\b", text, re.I)) for w in self.forbidden)
        return {"passive_voice_count": passive, "informal_usage": informal}