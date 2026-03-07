# utils/similarity_utils.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Union


def compute_tfidf_similarity(text1: str, text2: str) -> float:
    """
    Computes cosine similarity between two texts using TF-IDF vectors.
    Returns similarity as a percentage (0–100).
    """
    if not isinstance(text1, str) or not isinstance(text2, str):
        raise ValueError("Both inputs must be strings")
    
    if not text1.strip() or not text2.strip():
        return 0.0  # empty input, similarity is zero

    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),  # unigrams + bigrams
        min_df=1
    )

    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(float(similarity[0][0] * 100), 2)


def compute_cosine_similarity(vec1: Union[List[float], np.ndarray],
                              vec2: Union[List[float], np.ndarray]) -> float:
    """
    Computes cosine similarity between two numerical vectors.
    Returns percentage similarity (0–100).
    """
    vec1 = np.array(vec1).reshape(1, -1)
    vec2 = np.array(vec2).reshape(1, -1)

    if vec1.size == 0 or vec2.size == 0:
        return 0.0

    similarity = cosine_similarity(vec1, vec2)
    return round(float(similarity[0][0] * 100), 2)