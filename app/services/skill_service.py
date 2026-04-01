"""
Skill Service - Handles skill extraction and processing.

This module provides functions to clean, deduplicate, and process
skills extracted from LLM analysis.
"""


def extract_skills(llm_output: list) -> list:
    """
    Clean and deduplicate skills from LLM output.
    
    This function processes the raw list of skills from the LLM,
    removes duplicates, normalizes formatting, and filters out
    any invalid entries.
    
    Args:
        llm_output: List of skill names from the LLM analysis.
                   Example: ["Python", "python", "Machine Learning", "ML", ...]
    
    Returns:
        A cleaned, deduplicated list of skills.
        Example: ["Python", "Machine Learning", "SQL", "LLMs", "Data Analysis"]
    """
    # Define skill aliases/synonyms to consolidate similar skills
    # This helps merge variations of the same skill
    skill_aliases = {
        "python programming": "Python",
        "python3": "Python",
        "py": "Python",
        "ml": "Machine Learning",
        "machine-learning": "Machine Learning",
        "machine learning": "Machine Learning",
        "dl": "Deep Learning",
        "deep-learning": "Deep Learning",
        "deep learning": "Deep Learning",
        "nlp": "Natural Language Processing",
        "natural language processing": "Natural Language Processing",
        "js": "JavaScript",
        "javascript (js)": "JavaScript",
        "ts": "TypeScript",
        "react.js": "React",
        "reactjs": "React",
        "node": "Node.js",
        "nodejs": "Node.js",
        "node.js": "Node.js",
        "postgresql": "PostgreSQL",
        "postgres": "PostgreSQL",
        "aws cloud": "AWS",
        "amazon web services": "AWS",
        "azure cloud": "Azure",
        "microsoft azure": "Azure",
        "gcp": "GCP",
        "google cloud": "GCP",
        "google cloud platform": "GCP",
        "git version control": "Git",
        "github": "Git",
        "gitlab": "Git",
        "ci-cd": "CI/CD",
        "ci/cd": "CI/CD",
        "continuous integration": "CI/CD",
        "rest": "REST APIs",
        "restful": "REST APIs",
        "rest api": "REST APIs",
        "sql database": "SQL",
        "relational databases": "SQL",
        "problem-solving": "Problem Solving",
        "communication skills": "Communication",
    }
    
    # Track seen skills (case-insensitive) to remove duplicates
    seen_skills = set()
    cleaned_skills = []
    
    for skill in llm_output:
        # Skip empty or None values
        if not skill or not skill.strip():
            continue
        
        # Normalize the skill name
        skill_lower = skill.strip().lower()
        
        # Check if this is an alias for another skill
        normalized_skill = skill_aliases.get(skill_lower, skill.strip())
        
        # Normalize capitalization (title case for consistency)
        normalized_skill = normalized_skill.title()
        
        # Special cases for acronyms and specific formatting
        acronym_skills = ["SQL", "AWS", "GCP", "LLMs", "MLOps", "CI/CD", "REST APIs", "NLP", "Git"]
        if normalized_skill.upper() in [s.upper() for s in acronym_skills]:
            # Find the correct casing from the list
            for acronym in acronym_skills:
                if acronym.upper() == normalized_skill.upper():
                    normalized_skill = acronym
                    break
        
        # Check if we've already seen this skill (case-insensitive comparison)
        skill_key = normalized_skill.lower()
        if skill_key not in seen_skills:
            seen_skills.add(skill_key)
            cleaned_skills.append(normalized_skill)
    
    return cleaned_skills