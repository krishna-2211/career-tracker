# 🌊 Tech-Tsunami Career Tracker

A full-stack career roadmap generator built with **FastAPI** + **React**. Enter any tech role and get a structured learning roadmap with skills, prioritized tasks, and Notion sync — all powered by a modular Python backend.

---

## 📸 Features

- 🔍 **Role Analysis** — Search and analyze any tech career role
- ⚡ **Skill Extraction** — Identifies and deduplicates key skills for the role
- 🗺 **Learning Roadmap** — Generates prioritized tasks (Beginner / Intermediate / Advanced)
- ✅ **Progress Tracking** — Click tasks to mark them as done
- 📓 **Notion Sync** — Ready-to-connect Notion integration (currently mocked)
- 🎨 **Modern UI** — Two-column dark-mode interface built in React

---

## 🗂 Project Structure

```
MCP/
├── app/
│   ├── main.py                  # FastAPI app & routes
│   └── services/
│       ├── search_service.py    # Web search (Brave API ready)
│       ├── llm_service.py       # Skill extraction via LLM (OpenAI/Anthropic ready)
│       ├── skill_service.py     # Deduplication & normalization
│       ├── roadmap_service.py   # Learning roadmap generation
│       └── notion_service.py    # Notion integration
├── frontend/
│   ├── src/
│   │   ├── CareerTracker.jsx    # Main React component
│   │   ├── App.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── requirements.txt
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm

---

### Backend Setup

```bash
# 1. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn app.main:app --port 8001 --reload
```

Backend runs at: **http://localhost:8001**  
Swagger docs at: **http://localhost:8001/docs**

---

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check & version info |
| `GET` | `/health` | Server status |
| `POST` | `/analyze` | Analyze a career role |

### Example Request

```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"role": "AI Engineer"}'
```

### Example Response

```json
{
  "role": "AI Engineer",
  "skills": ["Python", "Machine Learning", "LLMs", "NLP", "Docker"],
  "roadmap": [
    {
      "task": "Learn Python basics (variables, loops, functions)",
      "skill": "Python",
      "status": "Not Started",
      "priority": "Beginner"
    }
  ],
  "notion_sync": {
    "success": true,
    "message": "Roadmap sent to Notion successfully (mock)",
    "tasks_created": 24,
    "role": "AI Engineer"
  }
}
```

---

## 🛠 Supported Roles

The following roles have pre-mapped skill sets out of the box:

| Role | Role | Role |
|------|------|------|
| AI Engineer | Data Scientist | ML Engineer |
| Software Engineer | Frontend Developer | Backend Developer |
| Full Stack Developer | DevOps Engineer | Cloud Engineer |
| Product Manager | | |

Any other role will fall back to a general skill set.

---

## 🔑 Connecting Real APIs (Optional)

All services are currently mocked. Here's how to wire up real APIs:

### Brave Search
In `app/services/search_service.py`:
```python
BRAVE_API_KEY = "your_key_here"
# Uncomment the requests.get(...) block
```

### LLM (OpenAI / Anthropic)
In `app/services/llm_service.py`:
```python
# Uncomment the openai.ChatCompletion.create(...) block
# Swap in your preferred provider and API key
```

### Notion
In `app/services/notion_service.py`:
```python
NOTION_API_KEY = "your_key_here"
DATABASE_ID = "your_database_id"
# Uncomment the notion_client block
```

Store all secrets in a `.env` file and load with `python-dotenv`:

```bash
pip install python-dotenv
```

```env
BRAVE_API_KEY=your_key
OPENAI_API_KEY=your_key
NOTION_API_KEY=your_key
NOTION_DATABASE_ID=your_id
```

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Uvicorn, Pydantic |
| Frontend | React 18, Vite, CSS-in-JS |
| Language | Python 3.10+, JavaScript (ES2022) |
| Integrations | Brave Search, OpenAI/Anthropic, Notion (all optional) |

---

## 📄 License

MIT License — feel free to use, modify, and distribute.
