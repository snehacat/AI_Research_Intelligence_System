"""
arXiv API Client - Free Research Paper Database Access
Rate Limit: Unlimited (but be reasonable)
"""

import requests
import feedparser
import re
import logging

from typing import Dict, List, Any
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logger = logging.getLogger(__name__)


class ArxivClient:

    def __init__(self):

        self.base_url = "https://export.arxiv.org/api/query"

        self.session = requests.Session()

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.session.headers.update({
            "User-Agent": "AI-Research-Intelligence-System/1.0"
        })

    def search_papers(
        self,
        query: str,
        max_results: int = 10,
        sort_by: str = "relevance"
    ) -> List[Dict]:

        """
        Search for papers on arXiv
        """

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")

        max_results = min(max_results, 100)

        try:

            params = {
                "search_query": query,
                "start": 0,
                "max_results": max_results,
                "sortBy": sort_by,
                "sortOrder": "descending"
            }

            response = self.session.get(
                self.base_url,
                params=params,
                timeout=10
            )

            response.raise_for_status()

            feed = feedparser.parse(response.content)

            papers = []

            entries = getattr(feed, "entries", [])

            for entry in entries:

                paper = {
                    "id": self._extract_arxiv_id(getattr(entry, "id", "")),
                    "title": getattr(entry, "title", "").replace("\n", " ").strip(),
                    "summary": getattr(entry, "summary", ""),
                    "authors": self._extract_authors(getattr(entry, "authors", [])),
                    "published": getattr(entry, "published", ""),
                    "updated": getattr(entry, "updated", ""),
                    "categories": self._extract_categories(entry),
                    "doi": self._extract_doi(entry),
                    "journal_ref": getattr(entry, "journal_ref", None),
                    "primary_category": self._extract_primary_category(entry),
                    "comments": getattr(entry, "comments", None),
                    "pdf_url": self._extract_pdf_url(entry),
                    "links": [
                        link.href
                        for link in getattr(entry, "links", [])
                        if hasattr(link, "href")
                    ]
                }

                papers.append(paper)

            return papers

        except requests.exceptions.RequestException as e:

            logger.error(f"Network error while querying arXiv: {str(e)}")
            return []

        except Exception:

            logger.exception("Unexpected arXiv search error")
            return []

    def get_paper_by_id(self, arxiv_id: str) -> Dict[str, Any]:

        """
        Get paper details by arXiv ID
        """

        try:

            query = f"id:{arxiv_id}"

            papers = self.search_papers(query, max_results=1)

            if papers:
                return papers[0]

            return {"error": f"Paper with ID {arxiv_id} not found"}

        except Exception as e:

            logger.error(f"Get paper by ID error: {str(e)}")
            return {"error": str(e)}

    def search_by_author(
        self,
        author_name: str,
        max_results: int = 10
    ) -> List[Dict]:

        query = f"au:{author_name}"
        return self.search_papers(query, max_results)

    def search_by_category(
        self,
        category: str,
        max_results: int = 10
    ) -> List[Dict]:

        query = f"cat:{category}"
        return self.search_papers(query, max_results)

    def search_recent_papers(
        self,
        category: str = "",
        days_back: int = 7,
        max_results: int = 20
    ) -> List[Dict]:

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        date_format = "%Y%m%d%H%M%S"

        start_str = start_date.strftime(date_format)
        end_str = end_date.strftime(date_format)

        query = f"submittedDate:[{start_str} TO {end_str}]"

        if category:
            query += f" AND cat:{category}"

        return self.search_papers(query, max_results, sort_by="submittedDate")

    def get_categories(self) -> Dict[str, List[str]]:

        return {
            "Computer Science": [
                "cs.AI", "cs.CL", "cs.CV", "cs.LG", "cs.ML",
                "cs.NE", "cs.CR", "cs.DS", "cs.DB", "cs.IR"
            ],
            "Mathematics": [
                "math.AG", "math.AT", "math.CA", "math.CO",
                "math.CV", "math.DG", "math.DS", "math.FA"
            ],
            "Physics": [
                "physics.comp-ph", "physics.data-an",
                "physics.app-ph", "cond-mat.stat-mech",
                "quant-ph", "hep-th", "astro-ph"
            ],
            "Quantitative Biology": [
                "q-bio.BM", "q-bio.CB", "q-bio.GN",
                "q-bio.MN", "q-bio.NC", "q-bio.QM"
            ],
            "Quantitative Finance": [
                "q-fin.CP", "q-fin.EC", "q-fin.GN",
                "q-fin.MF", "q-fin.PM", "q-fin.RM"
            ],
            "Statistics": [
                "stat.ML", "stat.ME", "stat.TH",
                "stat.AP", "stat.CO"
            ]
        }

    def _extract_arxiv_id(self, url: str) -> str:

        match = re.search(r"arxiv\.org\/abs\/([\w\.\-]+)", url)

        if match:

            arxiv_id = match.group(1)
            return arxiv_id.split("v")[0]

        return url

    def _extract_authors(self, authors: List) -> List[str]:

        return [
            getattr(author, "name", "")
            for author in authors
            if getattr(author, "name", "")
        ]

    def _extract_categories(self, entry) -> List[str]:

        categories = []

        if hasattr(entry, "tags"):

            for tag in entry.tags:

                if hasattr(tag, "term"):
                    categories.append(tag.term)

        return categories

    def _extract_primary_category(self, entry) -> str:

        if hasattr(entry, "arxiv_primary_category"):
            return getattr(entry.arxiv_primary_category, "term", "")

        return ""

    def _extract_doi(self, entry) -> str:

        if hasattr(entry, "doi"):
            return entry.doi

        for link in getattr(entry, "links", []):

            if hasattr(link, "href") and "doi.org" in link.href:
                return link.href.replace("https://doi.org/", "")

        return ""

    def _extract_pdf_url(self, entry) -> str:

        for link in getattr(entry, "links", []):

            if hasattr(link, "href") and (
                "/pdf/" in link.href or link.href.endswith(".pdf")
            ):
                return link.href

        return ""

    def get_paper_statistics(self, query: str) -> Dict[str, Any]:

        try:

            papers = self.search_papers(query, max_results=100)

            if not papers:
                return {"error": "No papers found"}

            categories_count = {}
            years_count = {}

            for paper in papers:

                for category in paper.get("categories", []):

                    categories_count[category] = (
                        categories_count.get(category, 0) + 1
                    )

                published = paper.get("published")

                year = "Unknown"

                if published and len(published) >= 4:
                    year = published[:4]

                years_count[year] = years_count.get(year, 0) + 1

            return {
                "total_papers": len(papers),
                "categories_distribution": categories_count,
                "years_distribution": years_count,
                "avg_authors_per_paper":
                    sum(len(p.get("authors", [])) for p in papers) / len(papers)
            }

        except Exception as e:

            logger.error(f"Statistics error: {str(e)}")
            return {"error": str(e)}