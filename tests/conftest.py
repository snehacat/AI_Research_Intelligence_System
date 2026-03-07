"""
Pytest configuration and shared fixtures for testing.
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_text():
    """Sample text for testing"""
    return """
    Artificial intelligence is transforming the world of research.
    Machine learning algorithms can analyze vast amounts of data.
    Natural language processing enables computers to understand human language.
    """


@pytest.fixture
def sample_reference_text():
    """Sample reference text for plagiarism testing"""
    return """
    Machine learning algorithms are revolutionizing data analysis.
    Artificial intelligence has significant impact on research methodologies.
    Computers can now process and understand natural language effectively.
    """


@pytest.fixture
def sample_document_words():
    """Sample document as word list"""
    return [
        "artificial", "intelligence", "transforming", "world", "research",
        "machine", "learning", "algorithms", "analyze", "vast",
        "amounts", "data", "natural", "language", "processing"
    ]


@pytest.fixture
def sample_reference_words():
    """Sample reference as word list"""
    return [
        "machine", "learning", "algorithms", "revolutionizing", "data",
        "analysis", "artificial", "intelligence", "significant", "impact",
        "research", "methodologies", "computers", "process", "understand"
    ]


@pytest.fixture
def sample_sentences():
    """Sample sentences for testing"""
    return [
        "Artificial intelligence is transforming research.",
        "Machine learning analyzes large datasets.",
        "Natural language processing understands text."
    ]


@pytest.fixture
def empty_text():
    """Empty text for edge case testing"""
    return ""


@pytest.fixture
def long_text():
    """Long text for performance testing"""
    return " ".join(["word"] * 10000)
