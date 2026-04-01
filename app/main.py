from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

from app.services.search_service import search_web
from app.services.llm_service import analyze_data
from app.services.skill_service import extract_skills
from app.services.roadmap_service import generate_roadmap
from app.services.sqlite_service import send_to_notion, get_all_roadmaps, update_task_status

app = FastAPI(
    title="Tech-Tsunami Innovation & Career Tracker",
    description="Live career analyzer — DuckDuckGo + Ollama + SQLite",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# ── Request / Response models ────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    role: str = Field(..., description="Target career role or interest area", min_length=1, max_length=150)


class AnalyzeResponse(BaseModel):
    role:        str
    skills:      list[str]
    roadmap:     list[dict]
    db_sync:     dict
    sources:     list[dict]


class TaskStatusRequest(BaseModel):
    task_id: int
    status:  str = Field(..., description="Not Started | In Progress | Completed")


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"name": "Tech-Tsunami Tracker", "version": "2.0.0", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_career_role(request: AnalyzeRequest):
    """
    Full pipeline:
      1. DuckDuckGo search (3 queries, ~15 results)
      2. Ollama LLM skill extraction
      3. Skill deduplication & normalization
      4. Roadmap generation
      5. SQLite persistence
    """
    try:
        role = request.role.strip()

        logging.info(f"[1/4] DuckDuckGo search → '{role}'")
        search_results = search_web(role)

        logging.info(f"[2/4] Ollama skill extraction → {len(search_results['results'])} snippets")
        raw_skills = analyze_data(search_results)

        logging.info(f"[3/4] Skill normalization → {len(raw_skills)} raw skills")
        skills = extract_skills(raw_skills)

        logging.info(f"[4/4] Roadmap + SQLite save → {len(skills)} skills")
        roadmap  = generate_roadmap(skills)
        db_sync  = send_to_notion(roadmap, role)

        sources = [
            {"title": r["title"], "url": r["url"]}
            for r in search_results.get("results", [])
            if r.get("url")
        ]

        return AnalyzeResponse(
            role=role,
            skills=skills,
            roadmap=roadmap,
            db_sync=db_sync,
            sources=sources,
        )

    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
def get_history():
    """Return all previously saved roadmaps from SQLite."""
    return {"roadmaps": get_all_roadmaps()}


@app.patch("/task/status")
def patch_task_status(body: TaskStatusRequest):
    """Update a single task's status in SQLite."""
    success = update_task_status(body.task_id, body.status)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid task_id or status")
    return {"success": True, "task_id": body.task_id, "status": body.status}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)