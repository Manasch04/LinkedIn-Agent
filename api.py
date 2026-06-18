import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.generator import generate_post
from src.researcher import research_and_generate
from src.utils import save_output

app = FastAPI(title="NB Media LinkedIn Agent")

OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "outputs")


class PostRequest(BaseModel):
    topic: str = ""
    post_type: str = "auto"
    mode: str = "manual"       # "manual" | "research"
    niche: str = "AI automation for businesses"


@app.post("/generate-post")
def generate(req: PostRequest):
    if req.mode == "research":
        result = research_and_generate(req.niche)
    else:
        if not req.topic:
            raise HTTPException(status_code=400, detail="topic is required for manual mode")
        result = generate_post(req.topic, req.post_type)

    save_output(result)
    return result


@app.get("/posts")
def list_posts():
    if not os.path.exists(OUTPUTS_DIR):
        return {"total": 0, "posts": []}

    files = sorted(
        [f for f in os.listdir(OUTPUTS_DIR) if f.endswith(".json")],
        reverse=True
    )
    posts = []
    for f in files[:20]:
        with open(os.path.join(OUTPUTS_DIR, f), encoding="utf-8") as fp:
            posts.append(json.load(fp))

    return {"total": len(files), "posts": posts}


@app.get("/health")
def health():
    return {"status": "ok"}


# Serve the UI — must be mounted last so API routes take priority
app.mount("/", StaticFiles(directory="static", html=True), name="static")
