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
├── main.py                  # CLI entry point
├── requirements.txt
├── .env.example
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
copy .env.example .env          # Windows
# cp .env.example .env          # macOS / Linux
# Then edit .env and fill in your keys
```

---

## Usage

```bash
python main.py
```

You will be prompted to choose a mode:

| Mode | Description |
|------|-------------|
| **1 — User Input** | Provide a topic yourself, pick a post type (or auto-detect) |
| **2 — Auto Research** | Tavily searches for trending topics; GPT picks the best one; post is generated |

At the end you can save the result as a JSON file in `outputs/`.

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
| `OPENRouter_API_KEY` | Yes | OpenRouter API key |
| `TAVILY_API_KEY` | Only for Auto Research mode | Tavily search API key |

---

## Architecture

See [docs/architecture.md](docs/architecture.md) for a detailed system design overview.
