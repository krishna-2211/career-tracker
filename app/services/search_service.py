"""
Search Service - Handles web search functionality using Brave Search API.

This module provides functions to search the web for information about
career roles and return simplified results.
"""

# Mock API key for demonstration purposes
# In production, this would be loaded from environment variables
BRAVE_API_KEY = "mock_brave_api_key"


def search_web(query: str) -> dict:
    """
    Search the web using Brave Search API for information about a career role.
    
    Args:
        query: The search query (typically a career role like "AI Engineer")
    
    Returns:
        A dictionary containing simplified search results with title and snippet only.
        Example: {
            "query": "AI Engineer",
            "results": [
                {"title": "What is an AI Engineer?", "snippet": "An AI engineer..."},
                ...
            ]
        }
    
    Note:
        This is currently using mock data. In production, you would make
        actual API calls to Brave Search API.
    """
    # Mock search results for demonstration
    # In production, you would use:
    # import requests
    # response = requests.get(
    #     "https://api.search.brave.com/res/v1/web/search",
    #     headers={"X-Subscription-Token": BRAVE_API_KEY},
    #     params={"q": query}
    # )
    # return response.json()
    
    mock_results = {
        "query": query,
        "results": [
            {
                "title": f"What is a {query}? - Complete Guide",
                "snippet": f"A {query} is a professional who specializes in designing, building, "
                          f"and maintaining systems related to this field. Key responsibilities "
                          f"include developing solutions, analyzing requirements, and collaborating "
                          f"with cross-functional teams."
            },
            {
                "title": f"Top Skills Required for a {query} in 2024",
                "snippet": f"Essential skills for a {query} include programming, problem-solving, "
                          f"data analysis, machine learning fundamentals, cloud computing, and "
                          f"strong communication abilities. Continuous learning is crucial."
            },
            {
                "title": f"How to Become a {query}: Career Path",
                "snippet": f"To become a successful {query}, start by learning core technical skills, "
                          f"build a strong portfolio, contribute to open-source projects, and "
                          f"stay updated with industry trends. A degree in computer science or "
                          f"related field is often preferred."
            },
            {
                "title": f"{query} Salary and Job Outlook",
                "snippet": f"The demand for {query} professionals is growing rapidly. Companies "
                          f"are looking for candidates with hands-on experience in modern tools "
                          f"and frameworks, strong analytical skills, and the ability to work "
                          f"in agile environments."
            },
            {
                "title": f"Best Resources to Learn {query} Skills",
                "snippet": f"Popular learning resources include online courses, bootcamps, "
                          f"documentation, and hands-on projects. Focus on building real-world "
                          f"applications to demonstrate your skills to potential employers."
            }
        ]
    }
    
    return mock_results