# backend/app/models.py
from sqlalchemy import Column, String, DateTime, Float, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship
import uuid

Base = declarative_base()

def gen_uuid():
    return str(uuid.uuid4())

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, nullable=True)
    filename = Column(String, nullable=False)
    text = Column(String, nullable=True)   # or Text
    parsed = Column(JSONB, nullable=True)
    embedding = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, default=gen_uuid)
    title = Column(String, nullable=True)
    jd_text = Column(String, nullable=False)
    parsed = Column(JSONB, nullable=True)
    embedding = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Match(Base):
    __tablename__ = "matches"
    id = Column(String, primary_key=True, default=gen_uuid)
    resume_id = Column(String, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    breakdown = Column(JSONB, nullable=True)  # stores embedding/skill/title/experience scores
    created_at = Column(DateTime(timezone=True), server_default=func.now())
