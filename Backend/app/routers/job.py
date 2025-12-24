from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

from app.services.parser import extract_skills, extract_title, estimate_experience_years
from app.core.config import IN_MEMORY_DB

router = APIRouter(prefix="/jobs", tags=["Jobs"])

class JobCreate(BaseModel):
    title: str | None = None
    description: str
    min_experience_years: int | None = None

@router.post("/")
def create_job(payload: JobCreate):
    if not payload.description or not payload.description.strip():
        raise HTTPException(status_code=400, detail="description is required")

    jd_text = payload.description
    # parse skills and title heuristically
    parsed = {
        "title": payload.title or extract_title(jd_text),
        "required_skills": extract_skills(jd_text),
        "min_experience_years": payload.min_experience_years or estimate_experience_years(jd_text)
    }

    job_id = str(uuid.uuid4())
    IN_MEMORY_DB["jobs"][job_id] = {
        "title": parsed["title"],
        "jd_text": jd_text,
        "parsed": parsed
    }

    return {
        "job_id": job_id,
        "parsed": parsed
    }
