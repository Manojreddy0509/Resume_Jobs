from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader
import io
import uuid

from app.services.parser import (
    extract_email, extract_phone, extract_skills, estimate_experience_years, extract_title
)
from app.core.config import IN_MEMORY_DB

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/")
async def upload_resume(file: UploadFile = File(...)):
    # Accept PDF only for now
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
        # scanned PDF or empty text
        parsed_data = {
            "email": None,
            "phone": None,
            "skills": [],
            "experience_years": None,
            "title": None,
            "ocr_required": True
        }
    else:
        parsed_data = {
            "email": extract_email(text),
            "phone": extract_phone(text),
            "skills": extract_skills(text),
            "experience_years": estimate_experience_years(text),
            "title": extract_title(text),
            "ocr_required": False
        }

    resume_id = str(uuid.uuid4())
    IN_MEMORY_DB["resumes"][resume_id] = {
        "filename": file.filename,
        "text": text,
        "parsed": parsed_data
    }

    return {
        "resume_id": resume_id,
        "filename": file.filename,
        "parsed": parsed_data,
        "text_preview": text[:1000]
    }
