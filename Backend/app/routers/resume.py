# backend/app/routers/resume.py  (replace relevant parts or whole file with this snippet)
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pypdf import PdfReader
import io

from app.services.parser import extract_email, extract_phone, extract_skills, estimate_experience_years, extract_title
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app.services.embeddings import embed_resume_text

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.get("/all")
async def list_resumes(db: AsyncSession = Depends(get_db)):
    """
    List all resumes for the dashboard.
    """
    resumes = await crud.get_all_resumes(db, limit=100)
    return resumes

@router.post("/")
async def upload_resume(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    pdf_bytes = await file.read()
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to read PDF")

    if not text.strip():
        parsed_data = { "email": None, "phone": None, "skills": [], "experience_years": None, "title": None, "ocr_required": True }
    else:
        parsed_data = {
            "email": extract_email(text),
            "phone": extract_phone(text),
            "skills": extract_skills(text),
            "experience_years": estimate_experience_years(text),
            "title": extract_title(text),
            "ocr_required": False
        }

    r = await crud.create_resume(db, filename=file.filename, text=text, parsed=parsed_data)

    # prepare normalized text for embedding (more signal = better embeddings)
    resume_text = (
        f"Candidate Title: {parsed_data.get('title')}\n"
        f"Skills: {', '.join(parsed_data.get('skills') or [])}\n"
        f"Experience: {parsed_data.get('experience_years')}\n\n"
        f"Resume Content:\n{text[:3000]}"
    )
    try:
        emb = await embed_resume_text(resume_text, parsed_data)
        if emb:
            await crud.update_resume_embedding(db, r.id, emb)
        else:
            print("resume embedding returned empty for", r.id)
    except Exception as e:
        print("Embedding error (resume):", e)

    resume = await crud.get_resume(db, r.id)
    return {
        "resume_id": resume.id,
        "filename": resume.filename,
        "parsed": resume.parsed,
        "text_preview": text[:1000]
    }
