"""
API Integration Testing Script
Tests all API integrations and shows their status
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from api_integrations.arxiv_client import ArxivClient
from api_integrations.crossref_client import CrossRefClient
from api_integrations.wikipedia_client import WikipediaClient
from api_integrations.language_tool_client import LanguageToolClient
from app.config import settings


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_status(api_name, status, message=""):
    """Print API status"""
    icon = "✅" if status else "❌"
    print(f"{icon} {api_name:20s} {'ACTIVE' if status else 'INACTIVE':10s} {message}")


def test_openai():
    """OpenAI API removed - paid service"""
    print_header("OpenAI API - REMOVED")
    print_status("OpenAI", False, "Paid service - removed from project")
    print("   ℹ️  All APIs in this project are FREE")
    return False


def test_semantic_scholar():
    """Semantic Scholar API removed - requires university email"""
    print_header("Semantic Scholar API - REMOVED")
    print_status("Semantic Scholar", False, "Requires university email verification")
    print("   ℹ️  This API has been removed from the project")
    return False


def test_arxiv():
    """Test arXiv API"""
    print_header("Testing arXiv API")
    
    client = ArxivClient()
    
    try:
        # Test search
        papers = client.search_papers("neural networks", max_results=3)
        
        if papers:
            print_status("arXiv", True, f"Found {len(papers)} papers")
            print("\n   Sample Results:")
            for i, paper in enumerate(papers[:2], 1):
                print(f"   {i}. {paper['title'][:60]}...")
                print(f"      Authors: {', '.join(paper['authors'][:2])}")
            return True
        else:
            print_status("arXiv", False, "No results returned")
            return False
            
    except Exception as e:
        print_status("arXiv", False, f"Error: {str(e)[:50]}")
        return False


def test_crossref():
    """Test CrossRef API"""
    print_header("Testing CrossRef API")
    
    client = CrossRefClient()
    
    try:
        # Test search
        refs = client.search_references("deep learning", limit=3)
        
        if refs:
            print_status("CrossRef", True, f"Found {len(refs)} references")
            print("\n   Sample Results:")
            for i, ref in enumerate(refs[:2], 1):
                print(f"   {i}. {ref['title'][:60]}...")
                print(f"      Journal: {ref['journal']}")
            return True
        else:
            print_status("CrossRef", False, "No results returned")
            return False
            
    except Exception as e:
        print_status("CrossRef", False, f"Error: {str(e)[:50]}")
        return False


def test_wikipedia():
    """Test Wikipedia API"""
    print_header("Testing Wikipedia API")
    
    client = WikipediaClient()
    
    try:
        # Test search
        articles = client.search_articles("machine learning", limit=3)
        
        if articles:
            print_status("Wikipedia", True, f"Found {len(articles)} articles")
            print("\n   Sample Results:")
            for i, article in enumerate(articles[:2], 1):
                print(f"   {i}. {article['title']}")
                print(f"      {article['description'][:60]}...")
            
            # Test common knowledge check
            test_text = "Water boils at 100 degrees Celsius at sea level."
            ck_result = client.check_common_knowledge(test_text)
            print(f"\n   Common Knowledge Test:")
            print(f"   Ratio: {ck_result.get('common_knowledge_ratio', 0):.2%}")
            
            return True
        else:
            print_status("Wikipedia", False, "No results returned")
            return False
            
    except Exception as e:
        print_status("Wikipedia", False, f"Error: {str(e)[:50]}")
        return False


def test_language_tool():
    """Test LanguageTool API"""
    print_header("Testing LanguageTool API")
    
    client = LanguageToolClient()
    
    try:
        # Test grammar check
        test_text = "This are a test sentence with grammar error."
        result = client.check_text(test_text)
        
        if result.get("success"):
            print_status("LanguageTool", True, f"Found {result['total_errors']} errors")
            print(f"\n   Test Text: {test_text}")
            print(f"   Errors Found: {result['total_errors']}")
            
            if result['suggestions']:
                print(f"\n   Sample Suggestion:")
                sug = result['suggestions'][0]
                print(f"   Original: '{sug['original']}'")
                print(f"   Suggestions: {', '.join(sug['suggestions'][:3])}")
            
            return True
        else:
            print_status("LanguageTool", False, result.get("error", "Unknown error"))
            return False
            
    except Exception as e:
        print_status("LanguageTool", False, f"Error: {str(e)[:50]}")
        return False


def show_configuration():
    """Show current configuration"""
    print_header("Current Configuration")
    
    api_status = settings.get_api_status()
    
    print("\n📋 API Keys Status:")
    print(f"   CrossRef:         {'✅ Configured' if api_status['crossref'] else '❌ Not configured'}")
    print(f"   arXiv:            ✅ Always active (no key needed)")
    print(f"   Wikipedia:        ✅ Always active (no key needed)")
    print(f"   LanguageTool:     ✅ Always active (no key needed)")
    
    print("\n⚙️  Analysis Settings:")
    print(f"   Analysis Depth:   {settings.default_analysis_depth.value}")
    print(f"   API Caching:      {'Enabled' if settings.enable_api_caching else 'Disabled'}")
    print(f"   Cache TTL:        {settings.cache_ttl_seconds}s")
    print(f"   Max References:   {settings.max_reference_papers}")
    
    print("\n🔒 Rate Limiting:")
    print(f"   Calls/Period:     {settings.api_rate_limit_calls}")
    print(f"   Period:           {settings.api_rate_limit_period}s")
    print(f"   Timeout:          {settings.api_timeout_seconds}s")
    print(f"   Max Retries:      {settings.api_max_retries}")


def main():
    """Main test function"""
    print("\n" + "=" * 70)
    print("  🔌 API INTEGRATION TEST SUITE")
    print("  AI Research Intelligence System - 100% FREE APIs")
    print("=" * 70)
    
    # Show configuration
    show_configuration()
    
    # Test all APIs
    results = {}
    
    results['arXiv'] = test_arxiv()
    results['Wikipedia'] = test_wikipedia()
    results['LanguageTool'] = test_language_tool()
    results['CrossRef'] = test_crossref()
    
    # Note about removed APIs
    print_header("Note: Removed APIs")
    print("   ℹ️  Semantic Scholar: Requires university email verification")
    print("   ℹ️  OpenAI: Paid service - not needed for core functionality")
    print("   ✅ All remaining APIs are 100% FREE!")
    
    # Summary
    print_header("Test Summary")
    
    active_count = sum(1 for status in results.values() if status)
    total_count = len(results)
    
    print(f"\n✅ Active APIs: {active_count}/{total_count}")
    print(f"❌ Inactive APIs: {total_count - active_count}/{total_count}")
    
    print("\n📊 Detailed Status:")
    for api, status in results.items():
        print_status(api, status)
    
    # Recommendations
    print("\n💡 System Status:")
    
    if active_count == total_count:
        print("   🎉 All FREE APIs are active! System fully operational.")
        print("   💰 Total cost: $0/month")
    elif active_count >= 3:
        print("   ✅ Core APIs are active. System is operational.")
        print("   💰 Total cost: $0/month")
    else:
        print("   ⚠️  Some APIs inactive. Check internet connection.")
    
    print("\n" + "=" * 70)
    print("  Test Complete! All APIs are FREE - No costs!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
