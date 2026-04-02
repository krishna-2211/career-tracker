from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

from app.services.search_service import search_web
from app.services.llm_service import analyze_data
from app.services.roadmap_service import generate_roadmap
from app.services.sqlite_service import send_to_notion, get_all_roadmaps, update_task_status
from app.services.memory_service import remember_analysis, remember_task_completed, remember_task_in_progress, get_memory_summary  # ← NEW

app = FastAPI(
    title="Tech-Tsunami Innovation & Career Tracker",
    description="Live career analyzer — Tavily + Ollama + SQLite + Memory",
    version="3.0.0",
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


class AnalyzeRequest(BaseModel):
    role: str = Field(..., min_length=1, max_length=150)


class AnalyzeResponse(BaseModel):
    role:        str
    skills:      list[str]
    roadmap:     list[dict]
    db_sync:     dict
    sources:     list[dict]
    memory:      dict        # ← NEW: memory summary included in every response


class TaskStatusRequest(BaseModel):
    task_id:  int
    status:   str = Field(..., description="Not Started | In Progress | Completed")
    task:     str = Field(default="", description="Task description (for memory)")
    skill:    str = Field(default="", description="Skill name (for memory)")
    role:     str = Field(default="", description="Role name (for memory)")


@app.get("/")
def root():
    return {"name": "Tech-Tsunami Tracker", "version": "3.0.0", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_career_role(request: AnalyzeRequest):
    try:
        role = request.role.strip()

        logging.info(f"[1/4] Tavily search → '{role}'")
        search_results = search_web(role)

        logging.info(f"[2/4] Ollama skill extraction → {len(search_results['results'])} snippets")
        skills = analyze_data(search_results)

        logging.info(f"[3/4] Roadmap generation → {len(skills)} skills")
        roadmap = generate_roadmap(skills)

        logging.info(f"[4/4] SQLite + Memory save → {len(roadmap)} tasks")
        db_sync = send_to_notion(roadmap, role)
        remember_analysis(role, skills, roadmap, db_sync.get("roadmap_id", -1))  # ← NEW

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
            memory=get_memory_summary(),   # ← NEW
        )

    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
def get_history():
    return {"roadmaps": get_all_roadmaps()}


@app.get("/memory")
def get_memory():
    """Return full memory summary — all roles, progress, skill gaps."""
    return get_memory_summary()


@app.patch("/task/status")
def patch_task_status(body: TaskStatusRequest):
    success = update_task_status(body.task_id, body.status)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid task_id or status")

    # Write to memory based on new status  ← NEW
    if body.status == "Completed":
        remember_task_completed(body.task_id, body.task, body.skill, body.role)
    elif body.status == "In Progress":
        remember_task_in_progress(body.task_id, body.task, body.skill, body.role)

    return {"success": True, "task_id": body.task_id, "status": body.status}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)