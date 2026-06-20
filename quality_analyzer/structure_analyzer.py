import re
from collections import Counter
from typing import Dict, List, Any
import logging

# List of common academic section headings
COMMON_HEADINGS = [
    "abstract",
    "introduction",
    "literature review",
    "related work",
    "methodology",
    "materials and methods",
    "experiments",
    "results",
    "discussion",
    "conclusion",
    "future work",
    "references",
]


def normalize_heading(line: str) -> str:
    """Normalize a heading line for comparison"""
    line = line.lower().strip()
    # Remove numbering e.g., "1. Introduction" -> "introduction"
    line = re.sub(r"^\d+\.\s*", "", line)
    return line


def analyze_structure(text: str) -> Dict[str, Any]:
    """
    Analyze research paper structure:
    - Section coverage
    - Paragraph distribution
    - Average paragraph length
    - Presence of common headings
    """

    if not text or not isinstance(text, str):
        logging.warning("Empty or invalid text provided to structure analyzer.")
        return {}

    # Split into paragraphs
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    total_paragraphs = len(paragraphs)

    paragraph_lengths = [len(p.split()) for p in paragraphs if len(p.split()) > 0]
    avg_paragraph_length = round(
        sum(paragraph_lengths) / len(paragraph_lengths), 2
    ) if paragraph_lengths else 0

    # Detect headings
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    headings_found = []
    for line in lines:
        normalized = normalize_heading(line)
        if normalized in COMMON_HEADINGS and normalized not in headings_found:
            headings_found.append(normalized)

    heading_coverage = round(len(headings_found) / len(COMMON_HEADINGS) * 100, 2)

    # Paragraph distribution
    short_paragraphs = len([l for l in paragraph_lengths if l < 50])
    medium_paragraphs = len([l for l in paragraph_lengths if 50 <= l <= 150])
    long_paragraphs = len([l for l in paragraph_lengths if l > 150])

    structure_report = {
        "total_paragraphs": total_paragraphs,
        "average_paragraph_length_words": avg_paragraph_length,
        "short_paragraphs": short_paragraphs,
        "medium_paragraphs": medium_paragraphs,
        "long_paragraphs": long_paragraphs,
        "headings_found": headings_found,
        "heading_coverage_percent": heading_coverage,
        "missing_headings": [
            h for h in COMMON_HEADINGS if h not in headings_found
        ],
    }

    return structure_report
