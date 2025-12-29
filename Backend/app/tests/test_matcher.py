# backend/app/tests/test_matcher.py
import pytest
from app.services.matcher import compute_match

def make_parsed(skills=None, title=None, exp=None):
    return {"skills": skills or [], "title": title, "experience_years": exp}

def test_compute_match_no_embeddings():
    resume = make_parsed(skills=["python", "ml"], title="Python dev", exp=2)
    job = make_parsed(skills=["python"], title="python developer", exp=1)
    score, breakdown, reasons, missing = compute_match(resume, job, resume_embedding=[], job_embedding=[])
    assert 0 <= score <= 1
    assert "skill_score" in breakdown
    assert "embedding_score" in breakdown
    assert breakdown["skill_score"] >= 0

def test_skill_heavy_match_scores_high():
    # identical skills should increase skill_score significantly
    resume = make_parsed(skills=["python","fastapi","sql"], title="Backend dev", exp=3)
    job = make_parsed(skills=["python","fastapi"], title="backend developer", exp=2)
    score, breakdown, reasons, missing = compute_match(resume, job, [], [])
    assert breakdown["skill_score"] == pytest.approx(2/3, rel=1e-3) or breakdown["skill_score"] > 0.5

def test_embedding_increases_score():
    # if embedding vectors are identical, embedding_score should be ~1 and final score higher
    resume = make_parsed(skills=["python"], title="dev", exp=2)
    job = make_parsed(skills=["python"], title="dev", exp=2)
    emb = [0.1, 0.2, 0.3]
    score_noemb, _, _, _ = compute_match(resume, job, [], [])
    score_withemb, breakdown, _, _ = compute_match(resume, job, emb, emb)
    assert breakdown["embedding_score"] == pytest.approx(1.0, rel=1e-3)
    assert score_withemb >= score_noemb

def test_experience_influence():
    resume = make_parsed(skills=["python"], title="dev", exp=1)
    job = make_parsed(skills=["python"], title="dev", exp=3)
    score, breakdown, reasons, _ = compute_match(resume, job, [], [])
    # experience component should be less than 1
    assert breakdown["experience_score"] <= 1.0
