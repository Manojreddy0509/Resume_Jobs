from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from app.models import Resume, Job, Match
from typing import Optional
from sqlalchemy.exc import NoResultFound
from sqlalchemy import update
from typing import List, Any

# Resume
async def create_resume(db: AsyncSession, filename: str, text: str, parsed: dict) -> Resume:
    r = Resume(filename=filename, text=text, parsed=parsed)
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return r

async def get_resume(db: AsyncSession, resume_id: str) -> Optional[Resume]:
    res = await db.get(Resume, resume_id)
    return res

async def get_all_resumes(db: AsyncSession, limit: int | None = None) -> List[Resume]:
    """
    Return list of Resume objects (most recent first). limit=None => all.
    """
    stmt = select(Resume).order_by(Resume.created_at.desc())
    if limit is not None:
        stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return rows

# Job
async def create_job(db: AsyncSession, title: str, jd_text: str, parsed: dict) -> Job:
    j = Job(title=title, jd_text=jd_text, parsed=parsed)
    db.add(j)
    await db.commit()
    await db.refresh(j)
    return j

async def get_job(db: AsyncSession, job_id: str) -> Optional[Job]:
    return await db.get(Job, job_id)

async def get_all_jobs(db: AsyncSession, limit: int | None = 100) -> List[Job]:
    stmt = select(Job).order_by(Job.created_at.desc())
    if limit is not None:
        stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# Match
async def create_match(db: AsyncSession, resume_id: str, job_id: str, score: float, breakdown: dict):
    m = Match(resume_id=resume_id, job_id=job_id, score=score, breakdown=breakdown)
    db.add(m)
    await db.commit()
    await db.refresh(m)
    return m



async def update_resume_embedding(db: AsyncSession, resume_id: str, embedding: List[float]):
    await db.execute(
        update(Resume).
        where(Resume.id == resume_id).
        values(embedding=embedding)
    )
    await db.commit()
    return await get_resume(db, resume_id)

async def update_job_embedding(db: AsyncSession, job_id: str, embedding: List[float]):
    await db.execute(
        update(Job).
        where(Job.id == job_id).
        values(embedding=embedding)
    )
    await db.commit()
    return await get_job(db, job_id)
