"""
Search Service - Live web search using DuckDuckGo (free, no API key).

Runs three targeted queries per role to surface:
  1. Required skills and tools (current year)
  2. Real job posting requirements
  3. Emerging trends in the role's domain

No account or API key needed — uses the duckduckgo-search package.
Install: pip install duckduckgo-search
"""

import logging
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

# Number of results to fetch per query
RESULTS_PER_QUERY = 5


def search_web(role: str) -> dict:
    """
    Search DuckDuckGo for live industry news, job requirements, and skills.

    Args:
        role: Target career role or interest area (e.g. "AI Engineer")

    Returns:
        {
            "query":   str,
            "results": [{"title": str, "snippet": str, "url": str}, ...]
        }
    """
    queries = [
        f"{role} required skills tools 2025",
        f"{role} job posting requirements responsibilities",
        f"{role} emerging trends industry 2025",
    ]

    all_results = []

    with DDGS() as ddgs:
        for query in queries:
            try:
                hits = list(
                    ddgs.text(query, max_results=RESULTS_PER_QUERY)
                )
                for h in hits:
                    all_results.append({
                        "title":   h.get("title", ""),
                        "snippet": h.get("body", ""),
                        "url":     h.get("href", ""),
                    })
                logger.info(f"DuckDuckGo: '{query}' → {len(hits)} results")

            except Exception as e:
                logger.error(f"DuckDuckGo search failed for '{query}': {e}")
                continue

    if not all_results:
        logger.warning("All DuckDuckGo queries failed — using mock results")
        return _mock_results(role)

    return {"query": role, "results": all_results}


def _mock_results(role: str) -> dict:
    """Fallback when DuckDuckGo is unreachable."""
    return {
        "query": role,
        "results": [
            {
                "title":   f"What is a {role}? — Complete Guide 2025",
                "snippet": (
                    f"A {role} designs and maintains AI-driven systems. "
                    "Key skills include Python, LLMs, RAG pipelines, FastAPI, "
                    "Docker, and cloud deployment on AWS or GCP."
                ),
                "url": "",
            },
            {
                "title":   f"Top Skills for {role} in 2025",
                "snippet": (
                    f"Employers hiring {role}s look for: prompt engineering, "
                    "fine-tuning LLMs, vector databases (Pinecone, ChromaDB), "
                    "MLOps, LangChain, and strong Python fundamentals."
                ),
                "url": "",
            },
            {
                "title":   f"{role} Job Postings — What Companies Want",
                "snippet": (
                    "Recent job descriptions emphasize agentic AI, tool use, "
                    "evaluation frameworks, SQL, REST API design, and the ability "
                    "to collaborate cross-functionally with product and data teams."
                ),
                "url": "",
            },
        ],
    }