# NB Media — LinkedIn Content Creation Agent

Generates LinkedIn posts in Nikit Bassi's exact writing style using GPT-4o.
Optionally auto-discovers trending topics via Tavily before generating.

---

## Project Structure

```
nb-media-linkedin-agent/
├── src/
│   ├── __init__.py          # Public API surface
│   ├── config.py            # API keys, model settings, system prompt
│   ├── generator.py         # Core post generation logic
│   ├── researcher.py        # Tavily research + topic selection
│   └── utils.py             # Save output to disk
├── tests/
│   ├── __init__.py
│   └── test_generator.py    # Unit tests (pytest)
├── outputs/                 # Generated posts saved here (gitignored)
├── docs/
│   └── architecture.md      # System design overview
├── static/
│   └── index.html           # Web UI served at /
├── main.py                  # CLI entry point
├── api.py                   # FastAPI backend — REST API + serves static UI
├── n8n_workflow_python_backend.json  # n8n workflow (import directly into n8n)
├── Procfile                 # Deployment process config (Railway / Heroku)
├── runtime.txt              # Python version pinned for deployment
├── requirements.txt
├── .env                     # API keys (not committed — see Environment Variables)
└── .gitignore
```

---

## Requirements

- Python 3.11+
- OpenRouter API key (GPT-4o)
- Tavily API key (only required for Auto Research mode)

---

## Setup

```bash
# 1. Clone / copy the project
cd nb-media-linkedin-agent

# 2. Create a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
# Create a .env file in the project root and add your keys:
# OPENROUTER_API_KEY=your_key_here
# TAVILY_API_KEY=your_key_here

# 5. Start the API server
uvicorn api:app --port 8000 --reload
```

The web UI will be available at `http://localhost:8000`.

---

## Usage

### CLI

```bash
python main.py
```

You will be prompted to choose a mode:

| Mode | Description |
|------|-------------|
| **1 — User Input** | Provide a topic yourself, pick a post type (or auto-detect) |
| **2 — Auto Research** | Tavily searches for trending topics; GPT picks the best one; post is generated |

At the end you can save the result as a JSON file in `outputs/`.

### REST API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/generate-post` | Generate a post (manual or research mode) |
| `GET` | `/posts` | List last 20 generated posts |
| `GET` | `/health` | Health check |

**Example request:**
```json
POST /generate-post
{
  "topic": "AI agents replacing manual workflows",
  "post_type": "tool_breakdown",
  "mode": "manual"
}
```

### n8n Workflow

Import `n8n_workflow_python_backend.json` directly into n8n.
The workflow includes two triggers:
- **Webhook** — generates a post on demand (user-provided topic)
- **7 AM scheduler** — auto-research mode, picks a trending topic and generates a post

---

## Post Types

| Key | Type | Description |
|-----|------|-------------|
| `internal_story` | NB Media Internal Story | First-person, "our team faced X" narrative |
| `founder_spotlight` | Founder Spotlight | Opens with "Meet [Name].", numbered steps |
| `tool_breakdown` | AI Tool/Stack Breakdown | Contrarian, specific, what we actually use |
| `contrarian` | Contrarian Take | Challenges a common belief |
| `auto` | Auto-detect | GPT picks the most suitable type |

---

## Running Tests

```bash
pytest tests/
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes | OpenRouter API key (access to GPT-4o) |
| `TAVILY_API_KEY` | Only for Auto Research mode | Tavily search API key |

---

## Architecture

See [docs/architecture.md](docs/architecture.md) for a detailed system design overview.
