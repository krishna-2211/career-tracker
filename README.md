# 🌊 Tech-Tsunami Career Tracker

A full-stack career roadmap generator built with **FastAPI** + **React** + **MCP**. Enter any tech role and get a structured learning roadmap with skills, prioritized tasks, and persistent memory — powered by live web search (Tavily), a local LLM (Ollama), and an MCP server that connects directly to Claude Desktop.

---

## ✨ Features

- 🔍 **Live Web Search** — Tavily MCP fetches real, up-to-date job market data (no mocks)
- 🤖 **Local LLM Extraction** — Ollama (llama3.2) extracts skills from search results, fully offline
- 🗺 **Learning Roadmap** — Prioritized tasks across Beginner / Intermediate / Advanced levels
- 🧠 **Persistent Memory** — Remembers every role analyzed, skill gaps, and task progress across sessions
- ✅ **Progress Tracking** — Mark tasks as Not Started / In Progress / Completed
- 🔌 **MCP Server** — Claude Desktop can call your pipeline directly as AI tools
- 💾 **SQLite Storage** — All roadmaps and tasks saved locally, no external database needed
- 🎨 **Modern UI** — Two-column dark-mode React interface

---

## 🗂 Project Structure

```
MCP/
├── app/
│   ├── main.py                  # FastAPI app & routes (v3.0.0)
│   ├── mcp_server.py            # MCP server — exposes pipeline as Claude tools
│   └── services/
│       ├── search_service.py    # Live web search via Tavily
│       ├── llm_service.py       # Skill extraction via Ollama (local LLM)
│       ├── roadmap_service.py   # Learning roadmap generation
│       ├── memory_service.py    # Persistent career memory (memory.json)
│       ├── sqlite_service.py    # SQLite persistence for roadmaps & tasks
│       └── skill_service.py     # (legacy — no longer used in pipeline)
├── frontend/
│   └── career-tracker/
│       └── src/
│           ├── CareerTracker.jsx  # Main React component
│           ├── App.jsx
│           └── index.css
├── requirements.txt
├── .env                         # API keys and config (create this)
├── roadmaps.db                  # SQLite database (auto-created)
├── memory.json                  # Persistent memory (auto-created)
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- [Ollama](https://ollama.com/download) installed and running
- A free [Tavily API key](https://tavily.com) (1000 searches/month free)

---

### 1. Ollama Setup

```bash
# Install Ollama from https://ollama.com/download, then pull the model
ollama pull llama3.2

# Ollama starts automatically after install, or run manually
ollama serve
```

---

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxx
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
SQLITE_DB_PATH=roadmaps.db
MEMORY_PATH=memory.json
```

```bash
# Start the backend
uvicorn app.main:app --port 8001 --reload
```

Backend runs at: **http://localhost:8001**  
Swagger docs at: **http://localhost:8001/docs**

---

### 3. Frontend Setup

```bash
cd frontend/career-tracker

npm install
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

### 4. MCP Server Setup (Claude Desktop)

Find your Claude Desktop config file:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Add the following (update `cwd` to your actual project path):

```json
{
  "mcpServers": {
    "career-tracker": {
      "command": "python",
      "args": ["-m", "app.mcp_server"],
      "cwd": "C:\\Users\\ASUS\\OneDrive\\Desktop\\GenAI for Business\\MCP"
    }
  }
}
```

Restart Claude Desktop. A 🔨 hammer icon in the chat input confirms the tools are connected.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Version info |
| `GET` | `/health` | Server status |
| `POST` | `/analyze` | Full pipeline — search → LLM → roadmap → save |
| `GET` | `/history` | All previously saved roadmaps from SQLite |
| `GET` | `/memory` | Persistent memory — roles, skill gaps, progress |
| `PATCH` | `/task/status` | Update a task's progress status |

### Example — Analyze a role

```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"role": "AI Engineer"}'
```

### Example — Update task progress

```bash
curl -X PATCH http://localhost:8001/task/status \
  -H "Content-Type: application/json" \
  -d '{"task_id": 3, "status": "In Progress", "task": "Learn Docker basics", "skill": "Docker", "role": "AI Engineer"}'
```

### Example — Check memory

```bash
curl http://localhost:8001/memory
```

```json
{
  "roles_analyzed": ["AI Engineer", "Cloud Engineer"],
  "total_sessions": 4,
  "completed_tasks_count": 6,
  "skill_gap": ["Docker", "MLOps", "Vector Databases"],
  "in_progress_tasks": [
    { "task_id": 3, "task": "Learn Docker basics", "skill": "Docker", "role": "AI Engineer" }
  ],
  "last_updated": "2026-04-01T18:51:33"
}
```

---

## 🧠 MCP Tools (Claude Desktop)

Once connected, Claude can call these tools directly in conversation:

| Tool | What it does |
|------|-------------|
| `analyze_career_role` | Full pipeline for a given role |
| `search_skills_for_role` | Raw web search results only |
| `generate_learning_roadmap` | Roadmap from a skills list |
| `get_career_history` | All saved roadmaps from SQLite |
| `get_memory_summary` | Full memory — all roles, gaps, progress |
| `get_role_memory` | Deep dive on one specific role |
| `update_task_progress` | Mark a task as In Progress or Completed |

**Example Claude prompts:**
> *"Analyze the career path for a Machine Learning Engineer"*  
> *"What roles have I researched before? What are my skill gaps?"*  
> *"Mark task 5 as completed"*  
> *"How far along am I on my Cloud Engineer roadmap?"*

---

## 🛠 Supported Roles (pre-mapped skills)

| Role | Role | Role |
|------|------|------|
| AI Engineer | Data Scientist | ML Engineer |
| Software Engineer | Frontend Developer | Backend Developer |
| Full Stack Developer | DevOps Engineer | Cloud Engineer |
| Product Manager | | |

Any other role will use the live Tavily search + Ollama extraction pipeline.

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Uvicorn, Pydantic |
| Frontend | React 18, Vite, CSS-in-JS |
| LLM | Ollama (llama3.2, local) |
| Search | Tavily API (MCP-compatible) |
| MCP Server | `mcp` Python SDK |
| Storage | SQLite (roadmaps), JSON (memory) |
| Language | Python 3.10+, JavaScript ES2022 |

---

## 📄 Copyright:

Krishna Panchal — feel free to use, modify, and distribute.
