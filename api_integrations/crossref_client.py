"""
Crossref API Client - Free Academic Citation and DOI Lookup
Rate Limit: ~1000 requests/day
"""

import requests
import logging
from typing import Dict, List, Any


class CrossRefClient:

    def __init__(self):

        self.base_url = "https://api.crossref.org"

        self.email = "snehakanswal2@gmail.com"

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "AI-Research-Intelligence-System/1.0",
            "Accept": "application/json"
        })

    def search_references(self, query: str, limit: int = 10) -> List[Dict]:

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")

        limit = min(limit, 100)

        try:

            url = f"{self.base_url}/works"

            params = {
                "query": query,
                "rows": limit,
                "select": "title,author,abstract,DOI,published,container-title,reference,type"
            }

            if self.email:
                params["mailto"] = self.email

            response = self.session.get(url, params=params, timeout=10)

            response.raise_for_status()

            data = response.json()

            works = data.get("message", {}).get("items", [])

            references = []

            for work in works:

                ref = {
                    "title": self._get_title(work),
                    "authors": self._get_authors(work),
                    "abstract": self._get_abstract(work),
                    "doi": self._get_doi(work),
                    "published": self._get_published_date(work),
                    "journal": self._get_journal(work),
                    "type": work.get("type", "journal-article"),
                    "references_count": len(work.get("reference", []))
                }

                references.append(ref)

            return references

        except requests.exceptions.RequestException as e:

            logging.error(f"Crossref network error: {str(e)}")
            return []

        except Exception:

            logging.exception("Unexpected Crossref search error")
            return []

    def validate_doi(self, doi: str) -> Dict[str, Any]:

        try:

            url = f"{self.base_url}/works/{doi}"

            response = self.session.get(url, timeout=10)

            response.raise_for_status()

            data = response.json()

            work = data.get("message", {})

            return {
                "valid": True,
                "title": self._get_title(work),
                "authors": self._get_authors(work),
                "abstract": self._get_abstract(work),
                "published": self._get_published_date(work),
                "journal": self._get_journal(work),
                "type": work.get("type", "unknown")
            }

        except Exception as e:

            return {
                "valid": False,
                "error": str(e),
                "doi": doi
            }

    def get_citation_count(self, doi: str) -> int:

        try:

            url = f"{self.base_url}/works/{doi}"

            response = self.session.get(url, timeout=10)

            response.raise_for_status()

            data = response.json()

            work = data.get("message", {})

            return work.get("is-referenced-by-count", 0)

        except Exception as e:

            logging.error(f"Citation count error: {str(e)}")

            return 0

    def search_by_author(self, author_name: str, limit: int = 10) -> List[Dict]:

        try:

            url = f"{self.base_url}/works"

            params = {
                "query.author": author_name,
                "rows": limit,
                "select": "title,author,abstract,DOI,published,container-title,type"
            }

            response = self.session.get(url, params=params, timeout=10)

            response.raise_for_status()

            data = response.json()

            works = data.get("message", {}).get("items", [])

            return [self._format_work(work) for work in works]

        except Exception as e:

            logging.error(f"Author search error: {str(e)}")

            return []

    def _format_work(self, work: Dict) -> Dict:

        return {
            "title": self._get_title(work),
            "authors": self._get_authors(work),
            "abstract": self._get_abstract(work),
            "doi": self._get_doi(work),
            "published": self._get_published_date(work),
            "journal": self._get_journal(work),
            "type": work.get("type", "journal-article")
        }

    def _get_title(self, work: Dict) -> str:

        title = work.get("title", [])

        return title[0] if title else "No title available"

    def _get_authors(self, work: Dict) -> List[str]:

        authors = work.get("author", [])

        author_names = []

        for author in authors or []:

            given = author.get("given", "")

            family = author.get("family", "")

            if given and family:
                author_names.append(f"{given} {family}")

            elif family:
                author_names.append(family)

        return author_names

    def _get_abstract(self, work: Dict) -> str:

        abstract = work.get("abstract", "")

        return abstract if abstract else "No abstract available"

    def _get_doi(self, work: Dict) -> str:

        return work.get("DOI", "")

    def _get_published_date(self, work: Dict) -> str:

        published = work.get("published", {})

        date_parts = published.get("date-parts", [])

        if date_parts and date_parts[0]:

            year = date_parts[0][0]

            month = date_parts[0][1] if len(date_parts[0]) > 1 else 1

            day = date_parts[0][2] if len(date_parts[0]) > 2 else 1

            return f"{year}-{month:02d}-{day:02d}"

        return "Unknown date"

    def _get_journal(self, work: Dict) -> str:

        container = work.get("container-title", [])

        return container[0] if container else "Unknown journal"