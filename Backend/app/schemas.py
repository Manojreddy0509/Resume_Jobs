from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ResumeCreateResponse(BaseModel):
    id: str
    filename: str
    parsed: Dict[str, Any]
    text_preview: Optional[str]

class JobCreate(BaseModel):
    title: Optional[str] = None
    description: str
    min_experience_years: Optional[int] = None

class JobCreateResponse(BaseModel):
    id: str
    parsed: Dict[str, Any]

class MatchRequest(BaseModel):
    resume_id: Optional[str] = None
    job_id: str

class MatchBreakdown(BaseModel):
    embedding_score: float
    skill_score: float
    title_score: float
    experience_score: float

class MatchResult(BaseModel):
    resume_id: str
    filename: Optional[str]
    score: float
    breakdown: MatchBreakdown
    reasons: List[str]
    missing_skills: List[str]
    label: str

class RankItem(BaseModel):
    resume_id: str
    filename: str
    score: float
    breakdown: Dict[str, float]
    reasons: List[str]
    missing_skills: List[str]
    label: str

class RankResponse(BaseModel):
    job_id: str
    results: List[RankItem]

class ExplanationResponse(BaseModel):
    score: float
    summary: str
    reasons: List[str]
    missing_skills: List[str]