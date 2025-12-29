# backend/app/services/matcher.py
from typing import Dict, Any, List, Tuple
import numpy as np
from app.services.parser import title_similarity

EPS = 1e-12


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    va = np.array(a, dtype=float)
    vb = np.array(b, dtype=float)
    na = va / (np.linalg.norm(va) + EPS)
    nb = vb / (np.linalg.norm(vb) + EPS)
    return float(np.clip(np.dot(na, nb), 0.0, 1.0))


def compute_match(
    resume_parsed: Dict[str, Any],
    job_parsed: Dict[str, Any],
    resume_embedding: List[float],
    job_embedding: List[float],
) -> Tuple[float, Dict[str, float], List[str], List[str]]:
    """
    RETURNS EXACTLY 4 VALUES — DO NOT CHANGE
    """

    # ---------- data ----------
    job_skills = set(job_parsed.get("required_skills", []))
    resume_skills = set(resume_parsed.get("skills", []))

    job_title = job_parsed.get("title", "")
    resume_title = resume_parsed.get("title", "")

    job_exp = job_parsed.get("min_experience_years")
    resume_exp = resume_parsed.get("experience_years")

    # ---------- scores ----------
    embedding_score = _cosine_similarity(job_embedding, resume_embedding)

    # Dynamic weights - ADJUSTED FOR GENEROUS SCORING
    w_embedding = 0.70
    w_skill = 0.20
    w_title = 0.05
    w_exp = 0.05

    if job_skills:
        # containment score: what % of job skills does candidate have?
        # Use sqrt to be more generous with partial matches (e.g. 1/4 = 0.25 -> 0.5)
        raw_skill = len(job_skills & resume_skills) / len(job_skills)
        skill_score = raw_skill ** 0.5
    else:
        # if job has no explicit skills parsed, rely more on embedding
        skill_score = 0.0
        w_embedding += w_skill
        w_skill = 0.0

    if job_title and resume_title:
        title_score = title_similarity(job_title, resume_title)
    else:
        # if missing titles, rely more on embedding
        title_score = 0.0
        w_embedding += w_title
        w_title = 0.0

    if job_exp is None or resume_exp is None:
        experience_score = 0.8 # Assume qualified if not specified
    elif resume_exp >= job_exp:
        experience_score = 1.0
    else:
        experience_score = resume_exp / max(job_exp, 1)

    # ---------- weighted sum ----------
    raw_final_score = (
        w_embedding * embedding_score +
        w_skill * skill_score +
        w_title * title_score +
        w_exp * experience_score
    )

    # Apply "Generous Curve" (Square Root) to boost lower scores
    # e.g. 0.3 -> 0.55, 0.5 -> 0.71, 0.8 -> 0.89
    final_score = raw_final_score ** 0.65  # Slight curve, not full sqrt
    
    # Baseline boost for any non-trivial match
    if final_score > 0.1:
        final_score += 0.15

    final_score = round(float(np.clip(final_score, 0.0, 1.0)), 4)

    breakdown = {
        "embedding_score": round(embedding_score, 4),
        "skill_score": round(skill_score, 4),
        "title_score": round(title_score, 4),
        "experience_score": round(experience_score, 4),
    }

    # ---------- explanations ----------
    reasons = []
    if embedding_score > 0.6:
        reasons.append("Strong semantic alignment between job description and resume.")
    elif embedding_score > 0.4:
        reasons.append("Good semantic overlap between job and resume.")

    if job_skills & resume_skills:
        reasons.append(f"Skills matched: {', '.join(sorted(job_skills & resume_skills))}.")

    if not reasons:
        reasons.append("Match computed using available resume and job data.")

    missing_skills = sorted(job_skills - resume_skills)


    return final_score, breakdown, reasons, missing_skills
