from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader
import io

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/")
async def upload_resume(file: UploadFile = File(...)):
    # 1. Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    # 2. Read file bytes
    pdf_bytes = await file.read()

    try:
        # 3. Extract text from PDF
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to read PDF"
        )

    # 4. Return extracted text (trim for now)
    return {
        "filename": file.filename,
        "text_preview": text[:1000]
    }
