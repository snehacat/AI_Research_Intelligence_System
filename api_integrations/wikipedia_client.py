"""
Wikipedia API Client - Free Common Knowledge Validation
Unlimited requests for academic common knowledge filtering
"""

import requests
import time
from typing import Dict, List, Optional, Any
import logging
import re

from spacy import language


class WikipediaClient:
    def __init__(self, language_code: str = "en"):
        """
        Initialize Wikipedia client

        Args:
            language_code: Wikipedia language code (en, es, fr, etc.)
        """
        self.base_url = f"https://{language_code}.wikipedia.org/api/rest_v1"
        self.api_url = f"https://{language_code}.wikipedia.org/w/api.php"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "AI-Research-Intelligence-System/1.0",
                "Accept": "application/json",
            }
        )

    def search_articles(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search Wikipedia articles

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of article summaries
        """
        try:
            url = f"{self.base_url}/page/summary"
            params = {"search": query, "limit": limit, "redirect": "true"}

            response = self.session.get(url, params=params)
            response.raise_for_status()

            articles = response.json()

            formatted_articles = []
            for article in articles:
                formatted_article = {
                    "title": article.get("title", ""),
                    "extract": article.get("extract", ""),
                    "url": article.get("content_urls", {})
                    .get("desktop", {})
                    .get("page", ""),
                    "thumbnail": article.get("thumbnail", {}).get("source", ""),
                    "description": article.get("description", ""),
                    "lang": article.get("lang", language_code),
                }
                formatted_articles.append(formatted_article)

            return formatted_articles

        except Exception as e:
            logging.error(f"Wikipedia search error: {str(e)}")
            return []

    def get_article_content(self, title: str) -> Dict[str, Any]:
        """
        Get full article content

        Args:
            title: Article title

        Returns:
            Article content and metadata
        """
        try:
            # Get article summary
            summary_url = f"{self.base_url}/page/summary/{title}"
            summary_response = self.session.get(summary_url)
            summary_response.raise_for_status()
            summary = summary_response.json()

            # Get article content
            content_url = f"{self.base_url}/page/html/{title}"
            content_response = self.session.get(content_url)
            content_response.raise_for_status()

            # Get article metadata
            metadata_url = f"{self.api_url}"
            metadata_params = {
                "action": "query",
                "prop": "extracts|info|categories",
                "titles": title,
                "explaintext": "true",
                "inprop": "url|displaytitle|lastrevid",
                "format": "json",
            }

            metadata_response = self.session.get(metadata_url, params=metadata_params)
            metadata_response.raise_for_status()
            metadata = metadata_response.json()

            # Extract article data
            pages = metadata.get("query", {}).get("pages", {})
            page_id = next(iter(pages.keys())) if pages else ""
            page_data = pages.get(page_id, {})

            return {
                "title": summary.get("title", ""),
                "extract": summary.get("extract", ""),
                "content": content_response.text,
                "full_text": page_data.get("extract", ""),
                "url": summary.get("content_urls", {})
                .get("desktop", {})
                .get("page", ""),
                "last_modified": page_data.get("touched", ""),
                "length": page_data.get("length", 0),
                "categories": [
                    cat["title"] for cat in page_data.get("categories", [])
                ],
                "page_id": page_id,
                "description": summary.get("description", ""),
                "thumbnail": summary.get("thumbnail", {}).get("source", ""),
            }

        except Exception as e:
            logging.error(f"Article content error: {str(e)}")
            return {"error": str(e)}

    def check_common_knowledge(self, text: str) -> Dict[str, Any]:
        """
        Check if text contains common knowledge that should be filtered
        from plagiarism detection

        Args:
            text: Text to analyze

        Returns:
            Common knowledge analysis
        """
        try:
            # Split text into sentences
            sentences = self._split_sentences(text)

            common_knowledge_sentences = []
            potential_facts = []

            for sentence in sentences:
                if len(sentence.strip()) < 20:  # Skip very short sentences
                    continue

                # Extract key terms from sentence
                key_terms = self._extract_key_terms(sentence)

                if key_terms:
                    # Search for each key term in Wikipedia
                    for term in key_terms[:2]:  # Limit to top 2 terms per sentence
                        articles = self.search_articles(term, limit=2)

                        for article in articles:
                            # Check if sentence content matches Wikipedia content
                            similarity = self._calculate_similarity(
                                sentence, article["extract"]
                            )

                            if similarity > 0.7:  # High similarity threshold
                                common_knowledge_sentences.append(
                                    {
                                        "sentence": sentence,
                                        "wikipedia_article": article["title"],
                                        "similarity": similarity,
                                        "article_url": article["url"],
                                        "matched_term": term,
                                    }
                                )
                                break

                # Also identify potential facts that might be common knowledge
                if self._is_potential_fact(sentence):
                    potential_facts.append(sentence)

            # Calculate common knowledge ratio
            total_sentences = len(
                [s for s in sentences if len(s.strip()) >= 20]
            )
            common_knowledge_ratio = len(common_knowledge_sentences) / max(
                total_sentences, 1
            )

            return {
                "total_sentences": total_sentences,
                "common_knowledge_sentences": common_knowledge_sentences,
                "potential_facts": potential_facts,
                "common_knowledge_ratio": round(common_knowledge_ratio, 3),
                "should_filter": common_knowledge_ratio
                > 0.1,  # Filter if >10% common knowledge
                "filter_suggestions": self._generate_filter_suggestions(
                    common_knowledge_sentences
                ),
            }

        except Exception as e:
            logging.error(f"Common knowledge check error: {str(e)}")
            return {"error": str(e)}

    def get_scientific_concepts(
        self, field: str, limit: int = 20
    ) -> List[Dict]:
        """
        Get scientific concepts from a specific field

        Args:
            field: Scientific field (e.g., "Machine learning", "Biology")
            limit: Maximum number of concepts

        Returns:
            List of scientific concepts with descriptions
        """
        try:
            # Search for field overview
            search_query = f"{field} concepts"
            articles = self.search_articles(search_query, limit)

            concepts = []
            for article in articles:
                # Only include articles that seem to be about concepts
                if any(
                    keyword in article["title"].lower()
                    for keyword in [
                        "concept",
                        "theory",
                        "principle",
                        "law",
                        "method",
                    ]
                ):
                    concepts.append(
                        {
                            "concept": article["title"],
                            "description": article["extract"],
                            "url": article["url"],
                            "category": "scientific_concept",
                        }
                    )

            # If not enough concept-specific articles, include general field articles
            if len(concepts) < limit:
                for article in articles:
                    if len(concepts) >= limit:
                        break

                    if article not in concepts:
                        concepts.append(
                            {
                                "concept": article["title"],
                                "description": article["extract"],
                                "url": article["url"],
                                "category": "general_knowledge",
                            }
                        )

            return concepts[:limit]

        except Exception as e:
            logging.error(f"Scientific concepts error: {str(e)}")
            return []

    def validate_factual_statements(self, statements: List[str]) -> List[Dict]:
        """
        Validate factual statements against Wikipedia

        Args:
            statements: List of factual statements to validate

        Returns:
            Validation results for each statement
        """
        results = []

        for statement in statements:
            try:
                # Extract key terms from statement
                key_terms = self._extract_key_terms(statement)

                validation_result = {
                    "statement": statement,
                    "key_terms": key_terms,
                    "wikipedia_matches": [],
                    "is_common_knowledge": False,
                    "confidence": 0.0,
                }

                for term in key_terms[:3]:  # Check top 3 terms
                    articles = self.search_articles(term, limit=2)

                    for article in articles:
                        similarity = self._calculate_similarity(
                            statement, article["extract"]
                        )

                        if similarity > 0.6:
                            validation_result["wikipedia_matches"].append(
                                {
                                    "article": article["title"],
                                    "similarity": similarity,
                                    "url": article["url"],
                                }
                            )

                # Determine if it's common knowledge
                if validation_result["wikipedia_matches"]:
                    validation_result["is_common_knowledge"] = True
                    validation_result["confidence"] = max(
                        match["similarity"]
                        for match in validation_result["wikipedia_matches"]
                    )

                results.append(validation_result)

                # Small delay to be respectful to Wikipedia servers
                time.sleep(0.1)

            except Exception as e:
                results.append(
                    {
                        "statement": statement,
                        "error": str(e),
                        "wikipedia_matches": [],
                        "is_common_knowledge": False,
                        "confidence": 0.0,
                    }
                )

        return results

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting - can be improved with NLTK
        sentences = re.split(r"[.!?]+", text)
        return [s.strip() for s in sentences if s.strip()]

    def _extract_key_terms(self, sentence: str) -> List[str]:
        """Extract key terms from sentence"""
        # Simple keyword extraction - look for capitalized words and technical terms
        words = sentence.split()
        key_terms = []

        for word in words:
            # Look for capitalized words (potential proper nouns)
            if word[0].isupper() and len(word) > 3:
                key_terms.append(word)

            # Look for technical terms (can be enhanced)
            if any(
                tech in word.lower()
                for tech in [
                    "algorithm",
                    "method",
                    "theory",
                    "system",
                    "process",
                ]
            ):
                key_terms.append(word)

        # Remove duplicates and short terms
        key_terms = list(set(key_terms))
        return [term for term in key_terms if len(term) > 2]

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple similarity between two texts"""
        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    def _is_potential_fact(self, sentence: str) -> bool:
        """Check if sentence might be a factual statement"""
        # Look for patterns that indicate facts
        fact_indicators = [
            "is",
            "are",
            "was",
            "were",
            "has",
            "have",
            "can",
            "will",
            "according to",
            "research shows",
            "studies indicate",
            "discovered",
            "found",
            "developed",
            "created",
        ]

        sentence_lower = sentence.lower()
        return any(indicator in sentence_lower for indicator in fact_indicators)

    def _generate_filter_suggestions(self, common_knowledge_sentences: List[Dict]) -> List[str]:
        """Generate suggestions for filtering common knowledge"""
        suggestions = []

        if common_knowledge_sentences:
            suggestions.append(
                f"Found {len(common_knowledge_sentences)} sentences that match common knowledge"
            )
            suggestions.append(
                "Consider excluding these from plagiarism detection"
            )
            suggestions.append("Focus on original analysis and unique insights")

            # Identify common topics
            topics = [s["wikipedia_article"] for s in common_knowledge_sentences]
            unique_topics = list(set(topics))

            if unique_topics:
                suggestions.append(
                    f"Common knowledge topics: {', '.join(unique_topics[:3])}"
                )

        return suggestions


# Test function
def test_wikipedia():
    """Test Wikipedia API integration"""
    client = WikipediaClient()

    # Test search
    print("=== Testing Wikipedia Search ===")
    results = client.search_articles("machine learning", limit=3)

    for i, article in enumerate(results, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Description: {article['description']}")
        print(f"   URL: {article['url']}")

    # Test common knowledge check
    print("\n=== Testing Common Knowledge Check ===")
    test_text = """
    Machine learning is a subset of artificial intelligence. Water boils at 100 degrees Celsius at sea level.
    The Earth revolves around the Sun. Python is a popular programming language for data science.
    """

    common_knowledge = client.check_common_knowledge(test_text)
    print(f"Common knowledge ratio: {common_knowledge['common_knowledge_ratio']}")
    print(f"Should filter: {common_knowledge['should_filter']}")
    print(
        f"Common knowledge sentences found: {len(common_knowledge['common_knowledge_sentences'])}"
    )

    for ck in common_knowledge["common_knowledge_sentences"]:
        print(f"  - '{ck['sentence']}' (matches: {ck['wikipedia_article']})")


if __name__ == "__main__":
    test_wikipedia()
