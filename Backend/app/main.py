from fastapi import FastAPI
from app.routers import resume, job, match

app = FastAPI(title="AI Resume Job Matcher - Dev")

app.include_router(resume.router)
app.include_router(job.router)
app.include_router(match.router)

@app.get("/health")
def health():
    return {"status": "ok"}