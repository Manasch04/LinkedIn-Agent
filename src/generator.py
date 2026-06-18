import requests
from datetime import datetime
from .config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_TEMPERATURE, OPENROUTER_MAX_TOKENS, NIKIT_SYSTEM_PROMPT


def _build_type_instruction(post_type: str) -> str:
    instructions = {
        "internal_story": "Write this as an NB Media internal story (first person, 'our team did X').",
        "founder_spotlight": "Write this as a Founder Spotlight post (start with 'Meet [Name].').",
        "tool_breakdown": "Write this as an AI tool/stack breakdown post.",
        "contrarian": "Write this as a contrarian take post (challenge a common belief).",
    }
    return instructions.get(post_type, "Choose the most suitable post type based on the topic.")


def _call_openrouter(system: str, user: str) -> str:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": OPENROUTER_TEMPERATURE,
            "max_tokens": OPENROUTER_MAX_TOKENS,
        },
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def _parse_output(raw: str) -> tuple[str, str]:
    if "---POST---" in raw and "---IMAGE CONCEPT---" in raw:
        parts = raw.split("---IMAGE CONCEPT---")
        post_text = parts[0].replace("---POST---", "").strip()
        image_concept = parts[1].strip()
    else:
        post_text = raw.strip()
        image_concept = "Not generated — re-run for image concept"
    return post_text, image_concept


def generate_post(topic: str, post_type: str = "auto") -> dict:
    """Generate a LinkedIn post in Nikit Bassi's style."""
    type_instruction = _build_type_instruction(post_type)

    user_prompt = f"""Topic: {topic}

{type_instruction}

Generate a complete LinkedIn post in Nikit Bassi's exact style.
Remember:
- Image text and post hook must have the SAME INTENT but DIFFERENT WORDS
- Image text = short, bold, punchy (6-10 words max)
- Post hook = slightly expanded, conversational version of the same idea
"""

    raw_output = _call_openrouter(NIKIT_SYSTEM_PROMPT, user_prompt)
    post_text, image_concept = _parse_output(raw_output)

    return {
        "topic": topic,
        "post_type": post_type,
        "post": post_text,
        "image_concept": image_concept,
        "generated_at": datetime.now().isoformat(),
    }
