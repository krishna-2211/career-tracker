"""
LLM Service - Skill extraction via Ollama (free, runs locally).

Feeds DuckDuckGo search results into a local Ollama model with a strict
prompt that filters hype and returns only concrete, employer-verified skills
as a JSON array.

Setup:
    1. Install Ollama : https://ollama.com/download
    2. Pull a model  : ollama pull llama3.2
    3. Ollama auto-starts after install, or run: ollama serve
"""

import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL", "llama3.2")

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a senior technical career analyst.

Your job: read raw search results about a career role and extract the most
important, concrete, employer-verified skills required for that role RIGHT NOW.

Rules:
- Return ONLY real, tangible technical or professional skills (tools, languages,
  frameworks, methodologies, soft skills).
- Filter out hype, buzzwords, and vague marketing language.
- Do NOT include company names, salary figures, or job titles.
- Return between 8 and 15 skills — no more, no less.
- Output ONLY a valid JSON array of strings. No explanation, no markdown, no
  extra text — just the raw JSON array starting with [ and ending with ].

Example output:
["Python", "LLMs", "RAG Pipelines", "FastAPI", "Docker", "SQL", "Prompt Engineering"]
"""


def analyze_data(search_results: dict) -> list:
    """
    Use a local Ollama model to extract skills from DuckDuckGo search results.

    Args:
        search_results: Output from search_service.search_web()

    Returns:
        List of skill name strings.
    """
    role     = search_results.get("query", "this role")
    snippets = "\n\n".join(
        f"[{r['title']}]\n{r['snippet']}"
        for r in search_results.get("results", [])
        if r.get("snippet")
    )

    user_message = (
        f"Career role: {role}\n\n"
        f"Live search results:\n{snippets}\n\n"
        f"Extract the key skills required for a {role}. "
        f"Return ONLY a JSON array of skill strings, nothing else."
    )

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model":  OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_message},
                ],
                "stream":  False,
                "options": {"temperature": 0.2, "num_predict": 500},
            },
            timeout=120,
        )
        response.raise_for_status()

        raw = response.json()["message"]["content"].strip()
        logger.info(f"Ollama raw output: {raw[:200]}")

        # Strip markdown fences if the model adds them
        raw = raw.strip("```json").strip("```").strip()

        # Extract just the JSON array in case there's surrounding text
        start = raw.find("[")
        end   = raw.rfind("]") + 1
        if start != -1 and end > start:
            raw = raw[start:end]

        skills = json.loads(raw)

        if isinstance(skills, list) and skills:
            logger.info(f"Ollama extracted {len(skills)} skills for '{role}'")
            return [str(s).strip() for s in skills if s]

        logger.warning("Ollama returned empty/invalid list — falling back to mock")
        return _mock_skills(role)

    except requests.exceptions.ConnectionError:
        logger.error(
            f"Cannot connect to Ollama at {OLLAMA_BASE_URL}. "
            "Start it with: ollama serve"
        )
        return _mock_skills(role)
    except requests.exceptions.Timeout:
        logger.error("Ollama timed out — falling back to mock skills")
        return _mock_skills(role)
    except json.JSONDecodeError as e:
        logger.error(f"Ollama output not valid JSON: {e} — falling back to mock")
        return _mock_skills(role)
    except Exception as e:
        logger.error(f"Ollama error: {e} — falling back to mock")
        return _mock_skills(role)


# ── Role-based mock fallback ────────────────────────────────────────────────

_MOCK_SKILL_SETS = {
    "ai engineer":        ["Python", "LLMs", "RAG Pipelines", "LangChain", "FastAPI", "Prompt Engineering", "Vector Databases", "Docker", "SQL", "Git"],
    "data scientist":     ["Python", "Machine Learning", "Statistics", "Pandas", "SQL", "Data Visualization", "scikit-learn", "Jupyter", "Tableau", "NumPy"],
    "ml engineer":        ["Python", "TensorFlow", "PyTorch", "MLOps", "Docker", "Kubernetes", "SQL", "Feature Engineering", "AWS SageMaker", "Git"],
    "software engineer":  ["Python", "JavaScript", "REST APIs", "Git", "SQL", "Docker", "System Design", "Agile", "Testing", "Cloud Computing"],
    "devops engineer":    ["Docker", "Kubernetes", "Terraform", "CI/CD", "AWS", "Linux", "Python", "Bash", "Monitoring", "Git"],
    "frontend developer": ["JavaScript", "React", "TypeScript", "CSS", "HTML", "Next.js", "Git", "Responsive Design", "Testing", "Webpack"],
    "backend developer":  ["Python", "Node.js", "SQL", "REST APIs", "Docker", "Microservices", "AWS", "Git", "Redis", "PostgreSQL"],
    "full stack developer": ["JavaScript", "Python", "React", "Node.js", "SQL", "MongoDB", "Docker", "AWS", "Git", "REST APIs"],
    "cloud engineer":     ["AWS", "Azure", "GCP", "Terraform", "Docker", "Kubernetes", "Python", "Linux", "Networking", "Security"],
    "product manager":    ["Product Strategy", "Agile", "Data Analysis", "SQL", "User Research", "A/B Testing", "Roadmapping", "Stakeholder Management", "Communication", "Jira"],
}


def _mock_skills(role: str) -> list:
    role_lower = role.lower()
    for key, skills in _MOCK_SKILL_SETS.items():
        if key in role_lower:
            return skills
    return ["Python", "Problem Solving", "Communication", "Git", "SQL", "Cloud Computing", "Agile", "REST APIs", "Docker", "Data Analysis"]