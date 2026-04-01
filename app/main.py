from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import logging

from app.services.search_service import search_web
from app.services.llm_service import analyze_data
from app.services.skill_service import extract_skills
from app.services.roadmap_service import generate_roadmap
from app.services.notion_service import send_to_notion
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Tech-Tsunami Innovation & Career Tracker",
    description="Analyze career roles and generate learning roadmaps",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AnalyzeRequest(BaseModel):
    role: str = Field(..., description="Target career role", min_length=1, max_length=100)

class AnalyzeResponse(BaseModel):
    role: str
    skills: list[str]
    roadmap: list[dict]
    notion_sync: dict

@app.get("/")
def root():
    return {"name": "Tech-Tsunami Tracker", "version": "1.0.0", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_career_role(request: AnalyzeRequest):
    try:
        role = request.role
        logging.info(f"[Step 1] Searching for: {role}")
        search_results = search_web(role)
        logging.info(f"[Step 2] Analyzing search results")
        raw_skills = analyze_data(search_results)
        skills = extract_skills(raw_skills)
        roadmap = generate_roadmap(skills)
        notion_result = send_to_notion(roadmap, role)
        return AnalyzeResponse(role=role, skills=skills, roadmap=roadmap, notion_sync=notion_result)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)