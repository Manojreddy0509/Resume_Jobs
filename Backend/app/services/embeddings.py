# backend/app/services/embeddings.py
import os
import asyncio
import requests
from typing import List, Optional
from app.core.config import settings

OPENROUTER_API_KEY = settings.openrouter_api_key
OPENROUTER_URL = "https://openrouter.ai/api/v1/embeddings"
# model name used by OpenRouter that proxies OpenAI embeddings
MODEL = settings.openai_embed_model

HEADERS = {
    "Content-Type": "application/json",
}

if OPENROUTER_API_KEY:
    HEADERS["Authorization"] = f"Bearer {OPENROUTER_API_KEY}"


def _prepare_text_for_embedding_for_resume(text: str, parsed: dict) -> str:
    parts = ["Candidate Resume"]
    if parsed:
        parts.append("Skills: " + ", ".join(parsed.get("skills") or []))
        parts.append("Experience: " + str(parsed.get("experience_years") or ""))
        parts.append("Title: " + (parsed.get("title") or ""))
    parts.append("Resume content:\n" + (text or "")[:3000])
    return "\n".join([p for p in parts if p])


def _prepare_text_for_embedding_for_job(jd_text: str, parsed: dict) -> str:
    parts = ["Job Posting"]
    if parsed:
        parts.append("Job Title: " + (parsed.get("title") or ""))
        parts.append("Required Skills: " + ", ".join(parsed.get("required_skills") or []))
        parts.append("Experience Required: " + str(parsed.get("min_experience_years") or ""))
    parts.append("Job Description:\n" + (jd_text or "")[:3000])
    return "\n".join([p for p in parts if p])


async def create_embedding(text: str) -> List[float]:
    """
    Returns embedding vector (list of floats) or empty list on failure.
    Uses requests in a thread to avoid blocking async loop.
    """
    if not text or text.strip() == "":
        print("create_embedding: empty text")
        return []

    if not OPENROUTER_API_KEY:
        print("create_embedding: OPENROUTER_API_KEY not set")
        return []

    payload = {"model": MODEL, "input": text[:8000]}

    def _call():
        try:
            r = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload, timeout=30)
            if r.status_code != 200:
                print("OpenRouter error:", r.status_code, r.text)
                return []
            dd = r.json()
            # OpenRouter returns structure similar to OpenAI: {"data":[{"embedding":[...]}], ...}
            return dd["data"][0]["embedding"]
        except Exception as e:
            print("create_embedding exception:", repr(e))
            return []

    vec = await asyncio.to_thread(_call)
    # ensure floats
    try:
        return [float(x) for x in vec] if vec else []
    except Exception:
        return []


async def embed_resume_text(text: str, parsed: dict):
    prepared = _prepare_text_for_embedding_for_resume(text, parsed)
    return await create_embedding(prepared)


async def embed_job_text(jd_text: str, parsed: dict):
    prepared = _prepare_text_for_embedding_for_job(jd_text, parsed)
    return await create_embedding(prepared)
