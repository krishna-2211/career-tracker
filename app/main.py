from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

from app.services.search_service import search_web
from app.services.llm_service import analyze_data
from app.services.skill_service import extract_skills
from app.services.roadmap_service import generate_roadmap
from app.services.sheets_service import send_to_notion  # Google Sheets MCP

app = FastAPI(
    title="Tech-Tsunami Innovation & Career Tracker",
    description="DuckDuckGo Search + Ollama LLM + Google Sheets — fully free stack",
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


class AnalyzeRequest(BaseModel):
    role: str = Field(
        ...,
        description="Target career role or interest area",
        min_length=1,
        max_length=150,
    )


class AnalyzeResponse(BaseModel):
    role:        str
    skills:      list[str]
    roadmap:     list[dict]
    notion_sync: dict         # kept as notion_sync so frontend needs no changes
    sources:     list[dict]   # DuckDuckGo result URLs


@app.get("/")
def root():
    return {
        "name":    "Tech-Tsunami Tracker",
        "version": "2.0.0",
        "stack":   "DuckDuckGo + Ollama + Google Sheets",
        "status":  "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_career_role(request: AnalyzeRequest):
    try:
        role = request.role.strip()

        logging.info(f"[1/4] DuckDuckGo search → '{role}'")
        search_results = search_web(role)

        logging.info(f"[2/4] Ollama skill extraction → {len(search_results['results'])} snippets")
        raw_skills = analyze_data(search_results)

        logging.info(f"[3/4] Skill normalization → {len(raw_skills)} raw skills")
        skills = extract_skills(raw_skills)

        logging.info(f"[4/4] Roadmap + Google Sheets sync → {len(skills)} skills")
        roadmap       = generate_roadmap(skills)
        sheets_result = send_to_notion(roadmap, role)

        # Surface source URLs to the frontend
        sources = [
            {"title": r["title"], "url": r["url"]}
            for r in search_results.get("results", [])
            if r.get("url")
        ]

        return AnalyzeResponse(
            role=role,
            skills=skills,
            roadmap=roadmap,
            notion_sync=sheets_result,
            sources=sources,
        )

    except Exception as e:
        logging.error(f"Error analyzing '{request.role}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)