# backend/app/routers/match.py
from fastapi import APIRouter, HTTPException, Depends, Path
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app import crud
from app.services.matcher import compute_match
from app.schemas import MatchResult, RankResponse
import math

router = APIRouter(prefix="/match", tags=["Matching"])


class MatchRequest(BaseModel):
    resume_id: Optional[str] = None
    job_id: str


@router.post("/", response_model=MatchResult)
async def match_single(payload: MatchRequest, db: AsyncSession = Depends(get_db)):
    if not payload.resume_id:
        raise HTTPException(status_code=422, detail="resume_id is required")

    job = await crud.get_job(db, payload.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")

    resume = await crud.get_resume(db, payload.resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="resume not found")

    job_parsed = job.parsed or {}
    resume_parsed = resume.parsed or {}

    final_score, breakdown, reasons, missing_skills = compute_match(
        resume_parsed=resume_parsed,
        job_parsed=job_parsed,
        resume_embedding=resume.embedding or [],
        job_embedding=job.embedding or [],
    )

    # persist match for analytics (best-effort)
    try:
        await crud.create_match(db, resume_id=resume.id, job_id=job.id, score=final_score, breakdown=breakdown)
    except Exception:
        pass

    # human summary label
    if final_score >= 0.7:
        label = "Excellent match"
    elif final_score >= 0.5:
        label = "Good match"
    elif final_score >= 0.35:
        label = "Partial match"
    else:
        label = "Low match"

    return MatchResult(
        resume_id=resume.id,
        filename=resume.filename,
        score=round(final_score, 4),
        breakdown=breakdown,
        reasons=reasons,
        missing_skills=missing_skills,
        label=label,
    )


@router.post("/job/{job_id}", response_model=RankResponse)
async def rank_job(
    job_id: str = Path(..., description="Job id to rank resumes for"),
    limit: Optional[int] = 50,
    db: AsyncSession = Depends(get_db),
):
    job = await crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")

    job_parsed = job.parsed or {}
    resumes = await crud.get_all_resumes(db, limit=500)
    if not resumes:
        return RankResponse(job_id=job_id, results=[])

    results = []
    for resume in resumes:
        resume_parsed = resume.parsed or {}
        final_score, breakdown, reasons, missing_skills = compute_match(
            resume_parsed=resume_parsed,
            job_parsed=job_parsed,
            resume_embedding=resume.embedding or [],
            job_embedding=job.embedding or [],
        )

        # determine label per resume (same bands)
        if final_score >= 0.7:
            label = "Excellent match"
        elif final_score >= 0.5:
            label = "Good match"
        elif final_score >= 0.35:
            label = "Partial match"
        else:
            label = "Low match"

        results.append(
            {
                "resume_id": resume.id,
                "filename": resume.filename,
                "score": round(final_score, 4),
                "breakdown": breakdown,
                "reasons": reasons,
                "missing_skills": missing_skills,
                "label": label,
            }
        )

        try:
            await crud.create_match(db, resume_id=resume.id, job_id=job_id, score=final_score, breakdown=breakdown)
        except Exception:
            pass

    sorted_results = sorted(results, key=lambda r: r["score"], reverse=True)[:limit]
    return RankResponse(job_id=job_id, results=sorted_results)