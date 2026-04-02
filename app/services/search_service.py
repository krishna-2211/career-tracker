"""
Search Service - Live web search via Tavily MCP.

Tavily is purpose-built for AI agents — reliable results, no rate-limit
surprises, and structured output. Free tier: 1000 searches/month.

Get API key: https://tavily.com
Add to .env:  TAVILY_API_KEY=tvly-xxxx
"""

import os
import logging
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

logger = logging.getLogger(__name__)

TAVILY_API_KEY  = os.getenv("TAVILY_API_KEY", "")
RESULTS_PER_QUERY = 5

# Initialise client once at import time
_client = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None


def search_web(role: str) -> dict:
    """
    Search the web for live job market data using Tavily.

    Runs three targeted queries per role:
      1. Required skills and tools
      2. Job posting requirements
      3. Emerging industry trends

    Args:
        role: Target career role (e.g. "AI Engineer")

    Returns:
        {"query": str, "results": [{"title": str, "snippet": str, "url": str}]}
    """
    if not _client:
        logger.warning("TAVILY_API_KEY not set — using mock results")
        return _mock_results(role)

    queries = [
        f"{role} required skills tools 2026",
        f"{role} job posting requirements responsibilities",
        f"{role} emerging trends industry 2026",
    ]

    all_results = []

    for query in queries:
        try:
            response = _client.search(
                query=query,
                max_results=RESULTS_PER_QUERY,
                search_depth="basic",        # "advanced" uses 2 credits vs 1
                include_answer=False,
            )
            hits = response.get("results", [])
            for h in hits:
                all_results.append({
                    "title":   h.get("title", ""),
                    "snippet": h.get("content", ""),
                    "url":     h.get("url", ""),
                })
            logger.info(f"Tavily: '{query}' → {len(hits)} results")

        except Exception as e:
            logger.error(f"Tavily search failed for '{query}': {e}")
            continue

    if not all_results:
        logger.warning("All Tavily queries failed — using mock results")
        return _mock_results(role)

    logger.info(f"Tavily: total {len(all_results)} results for '{role}'")
    return {"query": role, "results": all_results}


def _mock_results(role: str) -> dict:
    """Fallback when Tavily is unreachable or API key is missing."""
    return {
        "query": role,
        "results": [
            {
                "title":   f"What is a {role}? — Complete Guide 2026",
                "snippet": (
                    f"A {role} designs and maintains AI-driven systems. "
                    "Key skills include Python, LLMs, RAG pipelines, FastAPI, "
                    "Docker, and cloud deployment on AWS or GCP."
                ),
                "url": "",
            },
            {
                "title":   f"Top Skills for {role} in 2026",
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