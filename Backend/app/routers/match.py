from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/match")

class MatchRequest(BaseModel):
    resume_id: str
    job_id: str

@router.post("/")
def match_resume_job(payload: MatchRequest):
    # later: real matching logic
    return {
        "resume_id": payload.resume_id,
        "job_id": payload.job_id,
        "score": 0.82
    }