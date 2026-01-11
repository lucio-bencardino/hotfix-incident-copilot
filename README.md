# Hotfix Incident Copilot

**An AI-powered assistant that breaks down critical incident resolution into actionable, role-specific checklists.**

> *Built for the Technical Coding Challenge.*

## 🎯 The Problem & Solution
When a production incident occurs, cognitive load is high, and panic sets in. Engineers need immediate structure, not a chatty bot.

**Hotfix Incident Copilot** solves this by:
1.  **Reducing Panic:** Transforming a vague problem description into a structured JSON checklist.
2.  **Context Switching:** Adapting the remediation plan based on the user's role (Developer vs. DevOps/SRE).
3.  **Persistence:** Saving plans locally so they aren't lost if the browser refreshes during the chaos.

## 🛠 Tech Stack
- **Frontend:** Vue 3, Quasar Framework, TypeScript, Sass.
- **Backend:** Python, FastAPI, Pydantic.
- **AI Engine:** OpenAI.
- **Persistence:** LocalStorage (Browser).

## 🧠 Design & Architectural Decisions

### 1. Role-Based Prompting
Instead of a generic prompt, the system injects a specific "Persona" based on the user selection:
- **Developer:** Focuses on code, exceptions, library conflicts, and hotfixes.
- **DevOps/SRE:** Focuses on pods, latency, disk usage, and network configurations.
*Why?* A generic AI response is often too broad to be useful in a specific crisis.

### 2. Structured Output (JSON Mode)
The AI is forced to return JSON. This allows the Frontend to render a clean UI with checkboxes instead of a wall of markdown text.
*Why?* In an incident, readability is paramount. Steps must be actionable (clickable).

### 3. LocalStorage for History
*Trade-off:* I chose browser LocalStorage over a database for this MVP.
*Reasoning:* It allowed me to ship a robust "History/Recall" feature immediately without the overhead of setting up Postgres for the evaluator. It creates a "zero-setup" experience for testing.

## ⏱️ Time Spent & Trade-offs

**Total Time:** ~7 hours.

**Allocation:**
- **Product & Prompt Design:** Defining the "Roles" logic and refining system prompts.
- **Backend:** FastAPI setup, Pydantic models, OpenAI integration.
- **Frontend:** UI Components, Dark Mode, Markdown rendering, History logic.
- **Polish:** Refactoring, commit cleanup, README.

**Trade-offs made:**
- **No Database:** Used LocalStorage for simplicity and portability.
- **No Unit Tests:** Prioritized end-to-end functionality and type safety (TypeScript/Pydantic) over test coverage for the MVP timeframe.
- **No Auth:** Assumed an internal tool context.

## 🔮 Future Roadmap
While this MVP focuses on immediate incident triage, a production-ready version would include:

1.  **Multiplayer Collaboration (War Room):** Moving from LocalStorage to **PostgreSQL**. This would allow implementing User Authentication and Teams. Imagine a 'War Room' where multiple engineers login and update the *same* incident checklist in real-time.
2.  **Expanded Roles:** Adding more specialized personas, like a **Security Engineer** (for handling DDOS attacks or SQL injections) or a **DBA** (for specific database outages).
3.  **RAG Integration (Context Awareness):** Connecting the AI to internal documentation (Confluence, Notion) or past incident logs. This would allow the AI to say *"We saw this error 2 months ago, here is how we fixed it."*

## 🚀 How to Run

### Prerequisites
- Node.js (v20+)
- Python (v3.10+)

### 1. Backend Setup
Navigate to the backend folder:

```bash
cd backend
```

Create a .env file with the following content:
```ini
# AI CONFIG
AI_API_KEY=your_openai_api_key_here
AI_MODEL=gpt-4o-mini
AI_TEMPERATURE=0.7

# SECURITY & APP CONFIG
DEBUG=True
LOG_LEVEL=DEBUG
ENVIRONMENT=local
ALLOWED_ORIGINS=["http://localhost:9000"]
```

Install dependencies and run the server:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Server will start at http://localhost:8000

### 2. Frontend Setup
Open a new terminal, navigate to the frontend folder:
```bash
cd frontend
```

Create a .env file to point to the backend:
```ini
VITE_API_URL=http://localhost:8000/api/v1
```

Install dependencies and start the development server:
```bash
npm install
npm run dev
```
### 3. Usage
Open your browser at http://localhost:9000.

---
*Built by Lucio Bencardino*