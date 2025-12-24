from fastapi import FastAPI
from app.routers import resume
from app.routers import job
from app.routers import match


app = FastAPI(title="Resume Jobs Applying")
app.include_router(resume.router)
app.include_router(job.router)
app.include_router(match.router)


@app.get("/health")
def health():
    return {"status": "Good"}