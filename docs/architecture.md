# Architecture Overview

## System Design

```
User (CLI)
    │
    ▼
main.py  ──────────────────────────────────────────────────────┐
    │                                                           │
    ├── Mode 1: User Input                                      │
    │       │                                                   │
    │       ▼                                                   │
    │   src/generator.py                                        │
    │       │  generate_post(topic, post_type)                  │
    │       │                                                   │
    │       ├─ _build_type_instruction()   (formats the prompt) │
    │       ├─ _call_openai()              (HTTP → OpenAI API)  │
    │       └─ _parse_output()             (splits POST/IMAGE)  │
    │                                                           │
    └── Mode 2: Auto Research                                   │
            │                                                   │
            ▼                                                   │
        src/researcher.py                                       │
            │  research_and_generate(niche)                     │
            │                                                   │
            ├─ _search_trending()   (HTTP → Tavily API)         │
            ├─ _pick_best_topic()   (HTTP → OpenAI API)         │
            └─ generate_post()      (delegates to generator)    │
                                                                │
Both modes ─────────────────────────────────────────────────── ┘
    │
    ▼
src/utils.py
    │  save_output(result)
    └─ writes JSON to outputs/<timestamp>.json
```

## Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `config.py` | Single source of truth for API keys, model params, system prompt |
| `generator.py` | Builds the OpenAI prompt, calls the API, parses the structured response |
| `researcher.py` | Searches Tavily for trending topics, uses GPT to select the best one, delegates generation |
| `utils.py` | Saves results to disk; decoupled from generation so it can be replaced/extended |
| `main.py` | CLI orchestration only — no business logic |

## Data Flow

1. **Input**: topic string + post type enum
2. **Prompt Construction**: system prompt (Nikit persona) + user prompt (topic + type instruction)
3. **OpenAI Call**: GPT-4o returns a structured response with `---POST---` and `---IMAGE CONCEPT---` delimiters
4. **Parsing**: Response is split into `post` and `image_concept` fields
5. **Output**: dict with `topic`, `post_type`, `post`, `image_concept`, `generated_at`

## External Dependencies

| Service | Used For | Module |
|---------|----------|--------|
| OpenAI (GPT-4o) | Post generation & topic selection | `generator.py`, `researcher.py` |
| Tavily Search | Trending topic discovery | `researcher.py` |

## Key Design Decisions

- **Separation of config from logic**: `config.py` holds all magic strings/constants so changing the model or prompt only touches one file.
- **Thin CLI layer**: `main.py` contains no business logic — just I/O and routing.
- **Structured output via delimiters**: The system prompt instructs GPT to use `---POST---` / `---IMAGE CONCEPT---` delimiters, making parsing deterministic and testable.
- **`raise_for_status()` on every HTTP call**: Ensures HTTP errors surface immediately rather than silently producing malformed output.
