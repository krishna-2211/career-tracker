"""
SQLite Service - Local database storage (replaces Notion MCP).

Saves every roadmap task into a local SQLite database file.
No account, no API key, no internet — built into Python.

Database: roadmaps.db (auto-created on first run)
Tables:
    roadmaps  — one row per analysis session
    tasks     — one row per task, linked to a roadmap
"""

import os
import sqlite3
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("SQLITE_DB_PATH", "roadmaps.db")

logger = logging.getLogger(__name__)


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db(conn: sqlite3.Connection):
    """Create tables if they don't exist yet."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS roadmaps (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            role       TEXT NOT NULL,
            skills     TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            roadmap_id  INTEGER NOT NULL REFERENCES roadmaps(id),
            task        TEXT NOT NULL,
            skill       TEXT NOT NULL,
            priority    TEXT NOT NULL,
            status      TEXT NOT NULL DEFAULT 'Not Started',
            created_at  TEXT NOT NULL
        );
    """)
    conn.commit()


def send_to_notion(roadmap: list, role: str = "") -> dict:
    """
    Save roadmap tasks to the local SQLite database.

    This function is named send_to_notion to keep the interface
    identical to the original Notion service — no changes needed
    in main.py or anywhere else.

    Args:
        roadmap: List of task dicts from roadmap_service
        role:    Career role string

    Returns:
        {
            "success":       bool,
            "message":       str,
            "tasks_created": int,
            "role":          str,
            "db_path":       str,
            "roadmap_id":    int
        }
    """
    try:
        conn = _get_connection()
        _init_db(conn)

        now = datetime.utcnow().isoformat()

        # Insert roadmap session
        skills_str = ", ".join({t["skill"] for t in roadmap})
        cursor = conn.execute(
            "INSERT INTO roadmaps (role, skills, created_at) VALUES (?, ?, ?)",
            (role, skills_str, now),
        )
        roadmap_id = cursor.lastrowid

        # Insert all tasks
        task_rows = [
            (roadmap_id, t["task"], t["skill"], t["priority"], t.get("status", "Not Started"), now)
            for t in roadmap
        ]
        conn.executemany(
            "INSERT INTO tasks (roadmap_id, task, skill, priority, status, created_at) VALUES (?,?,?,?,?,?)",
            task_rows,
        )
        conn.commit()
        conn.close()

        message = f"Saved {len(roadmap)} tasks to SQLite (roadmap #{roadmap_id})"
        logger.info(message)

        return {
            "success":       True,
            "message":       message,
            "tasks_created": len(roadmap),
            "role":          role,
            "db_path":       DB_PATH,
            "roadmap_id":    roadmap_id,
        }

    except Exception as e:
        logger.error(f"SQLite error: {e}")
        return {
            "success":       False,
            "message":       f"SQLite error: {str(e)}",
            "tasks_created": 0,
            "role":          role,
            "db_path":       DB_PATH,
            "roadmap_id":    -1,
        }


def get_all_roadmaps() -> list:
    """Return all saved roadmaps with their tasks (used by /history endpoint)."""
    try:
        conn = _get_connection()
        _init_db(conn)

        roadmaps = conn.execute(
            "SELECT * FROM roadmaps ORDER BY created_at DESC"
        ).fetchall()

        result = []
        for rm in roadmaps:
            tasks = conn.execute(
                "SELECT * FROM tasks WHERE roadmap_id = ? ORDER BY priority",
                (rm["id"],),
            ).fetchall()
            result.append({
                "id":         rm["id"],
                "role":       rm["role"],
                "skills":     rm["skills"],
                "created_at": rm["created_at"],
                "tasks":      [dict(t) for t in tasks],
            })

        conn.close()
        return result

    except Exception as e:
        logger.error(f"SQLite read error: {e}")
        return []


def update_task_status(task_id: int, status: str) -> bool:
    """Update the status of a single task (Not Started / In Progress / Completed)."""
    valid_statuses = {"Not Started", "In Progress", "Completed"}
    if status not in valid_statuses:
        logger.error(f"Invalid status '{status}'")
        return False
    try:
        conn = _get_connection()
        conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"SQLite update error: {e}")
        return False