import requests
from .config import OPENROUTER_API_KEY, TAVILY_API_KEY, OPENROUTER_MODEL
from .generator import generate_post

_TOPIC_SELECTOR_SYSTEM = (
    "You are a LinkedIn content strategist for NB Media. "
    "Pick the single most engaging topic from the search results below for a LinkedIn post "
    "targeting founders and entrepreneurs. Return ONLY the topic as a 1-sentence description."
)


def _search_trending(niche: str) -> dict:
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query": f"latest news {niche} founders startups 2025",
            "search_depth": "basic",
            "max_results": 5,
            "include_answer": True,
        },
    )
    response.raise_for_status()
    return response.json()


def _pick_best_topic(results: list[dict]) -> str:
    summary = "\n".join(
        f"- {r['title']}: {r['content'][:200]}" for r in results
    )
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": _TOPIC_SELECTOR_SYSTEM},
                {
                    "role": "user",
                    "content": f"Search results:\n{summary}\n\nPick the best topic for a LinkedIn post.",
                },
            ],
            "temperature": 0.7,
            "max_tokens": 100,
        },
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def research_and_generate(niche: str = "AI automation for businesses") -> dict:
    """Search Tavily for trending topics, select the best one, then generate a post."""
    search_data = _search_trending(niche)
    results = search_data.get("results", [])

    best_topic = _pick_best_topic(results)
    result = generate_post(best_topic, post_type="auto")

    result["research_source"] = "Tavily Auto-Research"
    result["raw_search_results"] = [r["title"] for r in results]
    return result
