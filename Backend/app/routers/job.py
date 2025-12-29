# backend/app/routers/job.py (replace create_job function / file as needed)
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.services.parser import extract_skills, extract_title, estimate_experience_years
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app import crud
from app.services.embeddings import embed_job_text
from typing import List

router = APIRouter(prefix="/jobs", tags=["Jobs"])

class JobCreatePayload(BaseModel):
    title: Optional[str] = None
    description: str
    min_experience_years: Optional[int] = None

@router.get("/")
async def list_jobs(db: AsyncSession = Depends(get_db)):
    """
    List all jobs for the dashboard.
    """
    jobs = await crud.get_all_jobs(db, limit=100)
    return jobs

@router.post("/")
async def create_job(payload: JobCreatePayload, db: AsyncSession = Depends(get_db)):
    if not payload.description.strip():
        raise HTTPException(status_code=400, detail="description required")

    parsed = {
        "title": payload.title or extract_title(payload.description),
        "required_skills": extract_skills(payload.description),
        "min_experience_years": payload.min_experience_years or estimate_experience_years(payload.description)
    }

    j = await crud.create_job(db, title=parsed["title"], jd_text=payload.description, parsed=parsed)

    # prepare normalized job text for embedding
    job_text = (
        f"Job Title: {parsed['title']}\n"
        f"Required Skills: {', '.join(parsed.get('required_skills') or [])}\n"
        f"Experience Required: {parsed.get('min_experience_years')}\n\n"
        f"Job Description:\n{payload.description[:3000]}"
    )

    try:
        emb = await embed_job_text(job_text, parsed)
        if emb:
            await crud.update_job_embedding(db, j.id, emb)
        else:
            print("job embedding returned empty for", j.id)
    except Exception as e:
        print("Embedding error (job):", e)

    job = await crud.get_job(db, j.id)
    return {"job_id": job.id, "parsed": job.parsed}
