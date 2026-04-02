"""
Memory Service - Persistent career tracking across sessions.

Stores and retrieves:
  - Roles the user has analyzed
  - Skills identified per role
  - Task completion progress
  - Skill gap summary over time

Backed by a local JSON file (memory.json) — no extra dependencies.
Claude Desktop reads/writes this via MCP memory tools.
"""

import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MEMORY_PATH = os.getenv("MEMORY_PATH", "memory.json")
logger = logging.getLogger(__name__)


# ── Internal helpers ─────────────────────────────────────────────────────────

def _load() -> dict:
    """Load memory from disk, or return a fresh structure."""
    if os.path.exists(MEMORY_PATH):
        try:
            with open(MEMORY_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Memory load error: {e} — starting fresh")
    return {
        "roles_analyzed":   [],   # list of role strings ever analyzed
        "skill_history":    {},   # role → [skills]
        "completed_tasks":  [],   # list of {task, skill, role, completed_at}
        "in_progress_tasks":[],   # list of {task_id, task, skill, role}
        "sessions":         [],   # lightweight log of each analysis run
        "last_updated":     None,
    }


def _save(memory: dict):
    """Persist memory to disk."""
    memory["last_updated"] = datetime.utcnow().isoformat()
    try:
        with open(MEMORY_PATH, "w") as f:
            json.dump(memory, f, indent=2)
    except Exception as e:
        logger.error(f"Memory save error: {e}")


# ── Public API (called from mcp_server.py and main.py) ───────────────────────

def remember_analysis(role: str, skills: list, roadmap: list, roadmap_id: int):
    """
    Called after every successful /analyze run.
    Records the role, skills found, and opens task entries in memory.
    """
    memory = _load()
    now = datetime.utcnow().isoformat()

    # Track unique roles
    if role not in memory["roles_analyzed"]:
        memory["roles_analyzed"].append(role)

    # Store skill history per role (overwrite with latest)
    memory["skill_history"][role] = skills

    # Log the session
    memory["sessions"].append({
        "role":        role,
        "skills":      skills,
        "task_count":  len(roadmap),
        "roadmap_id":  roadmap_id,
        "analyzed_at": now,
    })

    _save(memory)
    logger.info(f"Memory: recorded analysis for '{role}' — {len(skills)} skills")


def remember_task_completed(task_id: int, task: str, skill: str, role: str):
    """Mark a task as completed in memory."""
    memory = _load()
    now = datetime.utcnow().isoformat()

    # Add to completed
    memory["completed_tasks"].append({
        "task_id":      task_id,
        "task":         task,
        "skill":        skill,
        "role":         role,
        "completed_at": now,
    })

    # Remove from in-progress if present
    memory["in_progress_tasks"] = [
        t for t in memory["in_progress_tasks"] if t.get("task_id") != task_id
    ]

    _save(memory)
    logger.info(f"Memory: task {task_id} completed — '{task}'")


def remember_task_in_progress(task_id: int, task: str, skill: str, role: str):
    """Mark a task as in-progress in memory."""
    memory = _load()

    # Avoid duplicates
    ids = [t.get("task_id") for t in memory["in_progress_tasks"]]
    if task_id not in ids:
        memory["in_progress_tasks"].append({
            "task_id": task_id,
            "task":    task,
            "skill":   skill,
            "role":    role,
        })
        _save(memory)
    logger.info(f"Memory: task {task_id} in progress — '{task}'")


def get_memory_summary() -> dict:
    """
    Return a structured summary of everything remembered.
    This is what Claude sees when it calls the get_memory MCP tool.
    """
    memory = _load()

    completed  = memory.get("completed_tasks", [])
    in_progress = memory.get("in_progress_tasks", [])
    sessions   = memory.get("sessions", [])

    # Skill gap: skills that appear in history but have no completed tasks
    all_skills = {
        skill
        for skills in memory.get("skill_history", {}).values()
        for skill in skills
    }
    completed_skills = {t["skill"] for t in completed}
    skill_gap = sorted(all_skills - completed_skills)

    return {
        "roles_analyzed":        memory.get("roles_analyzed", []),
        "total_roles":           len(memory.get("roles_analyzed", [])),
        "total_sessions":        len(sessions),
        "last_session":          sessions[-1] if sessions else None,
        "skills_across_roles":   memory.get("skill_history", {}),
        "completed_tasks_count": len(completed),
        "in_progress_count":     len(in_progress),
        "completed_tasks":       completed[-10:],   # last 10
        "in_progress_tasks":     in_progress,
        "skill_gap":             skill_gap,
        "last_updated":          memory.get("last_updated"),
    }


def get_role_memory(role: str) -> dict:
    """Return everything remembered about a specific role."""
    memory = _load()

    skills = memory.get("skill_history", {}).get(role, [])
    sessions = [s for s in memory.get("sessions", []) if s["role"] == role]
    completed = [t for t in memory.get("completed_tasks", []) if t["role"] == role]
    in_progress = [t for t in memory.get("in_progress_tasks", []) if t["role"] == role]

    completed_skills = {t["skill"] for t in completed}
    skill_gap = [s for s in skills if s not in completed_skills]

    return {
        "role":             role,
        "times_analyzed":   len(sessions),
        "last_analyzed":    sessions[-1]["analyzed_at"] if sessions else None,
        "skills":           skills,
        "skill_gap":        skill_gap,
        "completed_tasks":  completed,
        "in_progress_tasks": in_progress,
        "progress_pct":     round(len(completed_skills) / len(skills) * 100) if skills else 0,
    }