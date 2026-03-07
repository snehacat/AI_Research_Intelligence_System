"""
Semantic Scholar API Client - Free Paper Analysis and Citation Context
Rate Limit: 5000 requests/day
"""

import requests
import time
from typing import Dict, List, Optional, Any
import logging


class SemanticScholarClient:
    def __init__(self):
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AI-Research-Intelligence-System/1.0',
            'Accept': 'application/json'
        })
        
    def search_papers(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for academic papers using Semantic Scholar API
        
        Args:
            query: Search query (title, author, keywords)
            limit: Maximum number of results
            
        Returns:
            List of paper metadata
        """
        try:
            url = f"{self.base_url}/paper/search"
            params = {
                'query': query,
                'limit': limit,
                'fields': 'title,authors,abstract,year,citationCount,referenceCount,venue,journal,fieldsOfStudy,url'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            papers = data.get('data', [])
            
            formatted_papers = []
            for paper in papers:
                formatted_paper = {
                    'paperId': paper.get('paperId', ''),
                    'title': paper.get('title', ''),
                    'authors': self._format_authors(paper.get('authors', [])),
                    'abstract': paper.get('abstract', 'No abstract available'),
                    'year': paper.get('year', 'Unknown'),
                    'citationCount': paper.get('citationCount', 0),
                    'referenceCount': paper.get('referenceCount', 0),
                    'venue': paper.get('venue', 'Unknown venue'),
                    'journal': paper.get('journal', {}).get('name', 'Unknown journal') if paper.get('journal') else 'Unknown journal',
                    'fieldsOfStudy': paper.get('fieldsOfStudy', []),
                    'url': paper.get('url', ''),
                    'corpusId': paper.get('corpusId', '')
                }
                formatted_papers.append(formatted_paper)
                
            return formatted_papers
            
        except Exception as e:
            logging.error(f"Semantic Scholar search error: {str(e)}")
            return []
    
    def get_paper_details(self, paper_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific paper
        
        Args:
            paper_id: Semantic Scholar paper ID
            
        Returns:
            Detailed paper information
        """
        try:
            url = f"{self.base_url}/paper/{paper_id}"
            params = {
                'fields': 'title,authors,abstract,year,citationCount,referenceCount,venue,journal,fieldsOfStudy,url,references,citations'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            paper = response.json()
            
            return {
                'paperId': paper.get('paperId', ''),
                'title': paper.get('title', ''),
                'authors': self._format_authors(paper.get('authors', [])),
                'abstract': paper.get('abstract', 'No abstract available'),
                'year': paper.get('year', 'Unknown'),
                'citationCount': paper.get('citationCount', 0),
                'referenceCount': paper.get('referenceCount', 0),
                'venue': paper.get('venue', 'Unknown venue'),
                'journal': paper.get('journal', {}).get('name', 'Unknown journal') if paper.get('journal') else 'Unknown journal',
                'fieldsOfStudy': paper.get('fieldsOfStudy', []),
                'url': paper.get('url', ''),
                'references': self._format_references(paper.get('references', [])),
                'citations': self._format_citations(paper.get('citations', []))
            }
            
        except Exception as e:
            logging.error(f"Paper details error: {str(e)}")
            return {'error': str(e)}
    
    def get_citations(self, paper_id: str, limit: int = 100) -> List[Dict]:
        """
        Get papers that cite the given paper
        
        Args:
            paper_id: Semantic Scholar paper ID
            limit: Maximum number of citations to return
            
        Returns:
            List of citing papers
        """
        try:
            url = f"{self.base_url}/paper/{paper_id}/citations"
            params = {
                'limit': limit,
                'fields': 'title,authors,year,venue,journal,url'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            citations = data.get('data', [])
            
            formatted_citations = []
            for citation in citations:
                citing_paper = citation.get('citingPaper', {})
                formatted_citation = {
                    'paperId': citing_paper.get('paperId', ''),
                    'title': citing_paper.get('title', ''),
                    'authors': self._format_authors(citing_paper.get('authors', [])),
                    'year': citing_paper.get('year', 'Unknown'),
                    'venue': citing_paper.get('venue', 'Unknown venue'),
                    'url': citing_paper.get('url', '')
                }
                formatted_citations.append(formatted_citation)
                
            return formatted_citations
            
        except Exception as e:
            logging.error(f"Citations error: {str(e)}")
            return []
    
    def get_references(self, paper_id: str, limit: int = 100) -> List[Dict]:
        """
        Get papers referenced by the given paper
        
        Args:
            paper_id: Semantic Scholar paper ID
            limit: Maximum number of references to return
            
        Returns:
            List of referenced papers
        """
        try:
            url = f"{self.base_url}/paper/{paper_id}/references"
            params = {
                'limit': limit,
                'fields': 'title,authors,year,venue,journal,url'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            references = data.get('data', [])
            
            formatted_references = []
            for reference in references:
                cited_paper = reference.get('citedPaper', {})
                formatted_reference = {
                    'paperId': cited_paper.get('paperId', ''),
                    'title': cited_paper.get('title', ''),
                    'authors': self._format_authors(cited_paper.get('authors', [])),
                    'year': cited_paper.get('year', 'Unknown'),
                    'venue': cited_paper.get('venue', 'Unknown venue'),
                    'url': cited_paper.get('url', '')
                }
                formatted_references.append(formatted_reference)
                
            return formatted_references
            
        except Exception as e:
            logging.error(f"References error: {str(e)}")
            return []
    
    def search_by_author(self, author_name: str, limit: int = 10) -> List[Dict]:
        """
        Search for papers by author name
        
        Args:
            author_name: Author name to search
            limit: Maximum results
            
        Returns:
            List of papers by author
        """
        try:
            url = f"{self.base_url}/author/search"
            params = {
                'query': author_name,
                'limit': limit
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            authors = data.get('data', [])
            
            if not authors:
                return []
            
            # Get papers from first author match
            author_id = authors[0].get('authorId', '')
            if not author_id:
                return []
                
            return self.get_author_papers(author_id, limit)
            
        except Exception as e:
            logging.error(f"Author search error: {str(e)}")
            return []
    
    def get_author_papers(self, author_id: str, limit: int = 10) -> List[Dict]:
        """
        Get papers by author ID
        
        Args:
            author_id: Semantic Scholar author ID
            limit: Maximum results
            
        Returns:
            List of papers by author
        """
        try:
            url = f"{self.base_url}/author/{author_id}/papers"
            params = {
                'limit': limit,
                'fields': 'title,authors,abstract,year,citationCount,venue,journal,url'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            papers = data.get('data', [])
            
            return [self._format_paper(paper) for paper in papers]
            
        except Exception as e:
            logging.error(f"Author papers error: {str(e)}")
            return []
    
    def _format_authors(self, authors: List[Dict]) -> List[str]:
        """Format authors list"""
        author_names = []
        for author in authors:
            name = author.get('name', '')
            if name:
                author_names.append(name)
        return author_names
    
    def _format_references(self, references: List[Dict]) -> List[Dict]:
        """Format references list"""
        formatted_refs = []
        for ref in references:
            cited_paper = ref.get('citedPaper', {})
            formatted_ref = {
                'paperId': cited_paper.get('paperId', ''),
                'title': cited_paper.get('title', ''),
                'year': cited_paper.get('year', 'Unknown')
            }
            formatted_refs.append(formatted_ref)
        return formatted_refs
    
    def _format_citations(self, citations: List[Dict]) -> List[Dict]:
        """Format citations list"""
        formatted_cits = []
        for cit in citations:
            citing_paper = cit.get('citingPaper', {})
            formatted_cit = {
                'paperId': citing_paper.get('paperId', ''),
                'title': citing_paper.get('title', ''),
                'year': citing_paper.get('year', 'Unknown')
            }
            formatted_cits.append(formatted_cit)
        return formatted_cits
    
    def _format_paper(self, paper: Dict) -> Dict:
        """Format paper data"""
        return {
            'paperId': paper.get('paperId', ''),
            'title': paper.get('title', ''),
            'authors': self._format_authors(paper.get('authors', [])),
            'abstract': paper.get('abstract', 'No abstract available'),
            'year': paper.get('year', 'Unknown'),
            'citationCount': paper.get('citationCount', 0),
            'venue': paper.get('venue', 'Unknown venue'),
            'url': paper.get('url', '')
        }


# Test function
def test_semantic_scholar():
    """Test Semantic Scholar API integration"""
    client = SemanticScholarClient()
    
    # Test search
    print("=== Testing Semantic Scholar Search ===")
    results = client.search_papers("machine learning artificial intelligence", limit=3)
    
    for i, paper in enumerate(results, 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Authors: {', '.join(paper['authors'][:2])}")
        print(f"   Year: {paper['year']}")
        print(f"   Citations: {paper['citationCount']}")
        print(f"   Venue: {paper['venue']}")
    
    # Test paper details
    if results:
        print("\n=== Testing Paper Details ===")
        paper_id = results[0]['paperId']
        details = client.get_paper_details(paper_id)
        print(f"Paper: {details['title']}")
        print(f"Abstract: {details['abstract'][:100]}...")
        print(f"Total Citations: {details['citationCount']}")
        print(f"References: {details['referenceCount']}")


if __name__ == "__main__":
    test_semantic_scholar()
