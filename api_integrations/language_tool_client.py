"""
LanguageTool API Client - Grammar and Style Checking
Used for grammar validation in AI Research Intelligence System
"""

import requests
import logging
import re
from typing import Dict, List, Any, Optional


class LanguageToolClient:
    def __init__(self, language: str = "en-US"):
        self.base_url = "https://api.languagetoolplus.com/v2/check"

        self.language = language

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": "AI-Research-Intelligence-System/1.0",
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )

    def _empty_result(self, error_message: str):
        return {
            "success": False,
            "error": error_message,
            "corrections": [],
            "suggestions": [],
            "error_types": {},
            "total_errors": 0,
        }

    def check_text(
        self, text: str, additional_rules: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        if not text or not text.strip():
            return self._empty_result("Input text is empty")

        try:
            data = {
                "text": text,
                "language": self.language,
                "enabledOnly": "false",
            }

            if additional_rules:
                data["enabledRules"] = ",".join(additional_rules)

            response = self.session.post(self.base_url, data=data, timeout=10)

            response.raise_for_status()

            result = response.json()

            matches = result.get("matches", [])

            corrections = []
            suggestions = []
            error_types: Dict[str, int] = {}

            for match in matches:
                rule = match.get("rule", {})

                correction = {
                    "message": match.get("message", ""),
                    "short_message": match.get("shortMessage", ""),
                    "offset": match.get("offset", 0),
                    "length": match.get("length", 0),
                    "context": match.get("context", {}).get("text", ""),
                    "context_offset": match.get("context", {}).get("offset", 0),
                    "replacements": [
                        rep.get("value", "")
                        for rep in match.get("replacements", [])
                    ],
                    "rule_id": rule.get("id", ""),
                    "category": rule.get("category", {}).get("name", ""),
                    "type": rule.get("issueType", ""),
                    "severity": rule.get("isPremium", False),
                }

                corrections.append(correction)

                category = correction["category"]

                error_types[category] = error_types.get(category, 0) + 1

                offset = correction["offset"]
                length = correction["length"]

                original_text = ""

                if offset < len(text):
                    original_text = text[offset : offset + length]

                if correction["replacements"]:
                    suggestions.append(
                        {
                            "original": original_text,
                            "suggestions": correction["replacements"][:3],
                            "reason": correction["message"],
                        }
                    )

            return {
                "success": True,
                "corrections": corrections,
                "suggestions": suggestions,
                "error_types": error_types,
                "total_errors": len(corrections),
                "premium_errors": len([c for c in corrections if c["severity"]]),
                "free_errors": len([c for c in corrections if not c["severity"]]),
            }

        except requests.exceptions.RequestException as e:
            logging.error(f"LanguageTool network error: {str(e)}")
            return self._empty_result(str(e))

        except Exception as e:
            logging.exception("Unexpected LanguageTool error")
            return self._empty_result(str(e))

    def get_academic_style_suggestions(self, text: str) -> Dict[str, Any]:
        academic_rules = [
            "PASSIVE_VOICE",
            "WORDINESS",
            "REDUNDANCY",
            "FORMALITY",
            "COMMA_PARENTHESIS_WHITESPACE",
            "EN_QUOTES",
        ]

        result = self.check_text(text, academic_rules)

        if not result["success"]:
            return result

        academic_corrections = []
        academic_suggestions = []

        academic_categories = [
            "GRAMMAR",
            "STYLE",
            "TYPOGRAPHY",
            "PUNCTUATION",
        ]

        for correction in result["corrections"]:
            if correction["category"] in academic_categories:
                academic_corrections.append(correction)

        for suggestion in result["suggestions"]:
            if any(
                keyword in suggestion["reason"].upper()
                for keyword in ["PASSIVE", "INFORMAL", "WORDY"]
            ):
                academic_suggestions.append(suggestion)

        total_words = len(text.split())

        error_ratio = result["total_errors"] / max(total_words, 1)

        academic_score = max(0, min(100, 100 - (error_ratio * 100)))

        return {
            "success": True,
            "academic_corrections": academic_corrections,
            "academic_suggestions": academic_suggestions,
            "academic_score": round(academic_score, 1),
            "total_words": total_words,
            "error_ratio": round(error_ratio, 3),
            "needs_improvement": academic_score < 80,
        }

    def check_citations(self, text: str) -> Dict[str, Any]:
        result = self.check_text(text)

        if not result["success"]:
            return result

        citation_issues = []

        for correction in result["corrections"]:
            message = correction["message"].lower()

            if any(
                keyword in message
                for keyword in ["citation", "reference", "parenthesis", "quote"]
            ):
                citation_issues.append(correction)

        apa_matches = re.findall(r"\([A-Za-z]+,?\s*\d{4}\)", text)

        ieee_matches = re.findall(r"\[\d+\]", text)

        mla_matches = re.findall(r"\([A-Za-z]+\s*\d+\)", text)

        return {
            "success": True,
            "citation_issues": citation_issues,
            "detected_patterns": {
                "apa": apa_matches,
                "ieee": ieee_matches,
                "mla": mla_matches,
            },
            "total_citations": len(apa_matches) + len(ieee_matches) + len(mla_matches),
        }

    def get_readability_analysis(self, text: str) -> Dict[str, Any]:
        sentences = [s for s in text.split(".") if s.strip()]

        words = text.split()

        num_sentences = len(sentences)

        num_words = len(words)

        num_chars = sum(len(word) for word in words)

        avg_sentence_length = num_words / max(num_sentences, 1)

        avg_word_length = num_chars / max(num_words, 1)

        readability_score = 206.835 - (1.015 * avg_sentence_length) - (
            84.6 * avg_word_length
        )

        return {
            "success": True,
            "metrics": {
                "sentence_count": num_sentences,
                "word_count": num_words,
                "character_count": num_chars,
                "avg_sentence_length": round(avg_sentence_length, 1),
                "avg_word_length": round(avg_word_length, 1),
                "readability_score": round(readability_score, 1),
            },
            "readability_level": self._get_readability_level(readability_score),
            "suggestions": self._get_readability_suggestions(
                avg_sentence_length, avg_word_length
            ),
        }

    def _get_readability_level(self, score: float) -> str:
        if score >= 90:
            return "Very Easy"

        elif score >= 80:
            return "Easy"

        elif score >= 70:
            return "Fairly Easy"

        elif score >= 60:
            return "Standard"

        elif score >= 50:
            return "Fairly Difficult"

        elif score >= 30:
            return "Difficult"

        return "Very Difficult"

    def _get_readability_suggestions(
        self, avg_sentence_length: float, avg_word_length: float
    ) -> List[str]:
        suggestions = []

        if avg_sentence_length > 20:
            suggestions.append("Break long sentences into shorter ones")

        if avg_word_length > 6:
            suggestions.append("Use simpler words where possible")

        if not suggestions:
            suggestions.append("Text readability is good")

        return suggestions
