from fastapi import APIRouter

router = APIRouter(prefix="/jobs")

@router.post("/")
def create_job():
    return {"message": "job created (dummy)"}
