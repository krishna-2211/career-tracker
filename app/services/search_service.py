"""
Search Service - Handles web search functionality using DuckDuckGo MCP.

This module fetches live search results for career roles using a free MCP endpoint.
"""

import requests

DUCKDUCKGO_MCP_URL = "https://api.duckduckgo.com/?q={query}&format=json"  # free public MCP

def search_web(query: str) -> dict:
    """
    Search the web using DuckDuckGo MCP for information about a career role.
    
    Args:
        query: The search query (e.g., "AI Engineer")
    
    Returns:
        A dictionary containing search results with title and snippet.
    """
    try:
        response = requests.get(DUCKDUCKGO_MCP_URL.format(query=query))
        data = response.json()
        
        # DuckDuckGo returns 'RelatedTopics' as a list of results
        results = []
        for topic in data.get("RelatedTopics", []):
            if "Text" in topic and "FirstURL" in topic:
                results.append({
                    "title": topic.get("Text"),
                    "snippet": topic.get("Text")[:250]  # limit snippet length
                })
        
        # Return in same format as previous mock
        return {
            "query": query,
            "results": results[:5]  # limit to top 5 results
        }
    except Exception as e:
        # Fallback to mock if the MCP fails
        print(f"Error fetching from DuckDuckGo MCP: {e}")
        return {
            "query": query,
            "results": [
                {"title": f"{query} - search failed", "snippet": str(e)}
            ]
        }