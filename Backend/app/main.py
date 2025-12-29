from fastapi import FastAPI
from app.routers import resume, job, match
from app.db import database
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router)
app.include_router(job.router)
app.include_router(match.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
