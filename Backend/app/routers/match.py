from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import IN_MEMORY_DB
from app.services.parser import title_similarity

router = APIRouter(prefix="/match", tags=["Matching"])

class MatchRequest(BaseModel):
    resume_id: str | None = None
    job_id: str | None = None

@router.post("/")
def match_resume_job(payload: MatchRequest):
    # two modes: resume_id + job_id => single pair
    # recruiter-style: job_id only => top resumes (handled here if resume_id None)
    if not payload.job_id:
        raise HTTPException(status_code=400, detail="job_id is required")

    job = IN_MEMORY_DB["jobs"].get(payload.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")

    job_parsed = job["parsed"]
    job_skills = set(job_parsed.get("required_skills", []))
    job_title = job_parsed.get("title")
    job_min_exp = job_parsed.get("min_experience_years")

    results = []

    # If a specific resume_id is provided, only return that match
    resumes = [ (payload.resume_id, IN_MEMORY_DB["resumes"].get(payload.resume_id)) ] if payload.resume_id else list(IN_MEMORY_DB["resumes"].items())

    for rid, rdata in resumes:
        if rdata is None:
            continue
        parsed = rdata["parsed"]
        resume_skills = set(parsed.get("skills", []))
        resume_title = parsed.get("title")
        resume_exp = parsed.get("experience_years")

        # skill score (Jaccard)
        union = job_skills.union(resume_skills)
        inter = job_skills.intersection(resume_skills)
        skill_score = (len(inter) / len(union)) if union else 0.0

        # title similarity (SequenceMatcher)
        title_score = title_similarity(job_title or "", resume_title or "")

        # experience score
        exp_score = 0.0
        if job_min_exp is None or resume_exp is None:
            exp_score = 0.5  # neutral when missing
        else:
            # if resume_exp >= job_min_exp => 1.0 else fraction (resume_exp / job_min_exp)
            exp_score = 1.0 if resume_exp >= job_min_exp else (resume_exp / job_min_exp)

        # final weighted score
        final_score = 0.6 * skill_score + 0.25 * title_score + 0.15 * exp_score

        results.append({
            "resume_id": rid,
            "filename": rdata.get("filename"),
            "score": round(final_score, 4),
            "breakdown": {
                "skill_score": round(skill_score, 4),
                "title_score": round(title_score, 4),
                "experience_score": round(exp_score, 4)
            },
            "matched_skills": sorted(list(inter)),
            "missing_skills": sorted(list(job_skills - resume_skills))
        })

    # sort by score desc
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    # If single resume requested, return single result
    if payload.resume_id:
        if results:
            return results[0]
        raise HTTPException(status_code=404, detail="resume not found")

    # recruiter-style: return top-k (k=10)
    return {"job_id": payload.job_id, "results": results[:10]}
