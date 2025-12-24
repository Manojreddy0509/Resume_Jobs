import io
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import IN_MEMORY_DB

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_resume_upload_and_job_and_match(tmp_path):
    # create a simple PDF in memory — produce a minimal PDF via bytes (pypdf can read simple text PDF)
    # For speed, we will upload a small PDF file present locally or use a text trick.
    # Here we'll create a tiny PDF using reportlab if not available, otherwise skip - but we test via fallback simple text file with proper content_type bypass.
    pdf_bytes = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << >> /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 100 700 Td (john.doe@example.com) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000123 00000 n \n0000000223 00000 n \ntrailer\n<< /Root 1 0 R >>\nstartxref\n333\n%%EOF"
    files = {"file": ("resume.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    r = client.post("/resumes/", files=files)
    assert r.status_code == 200
    resp = r.json()
    resume_id = resp["resume_id"]
    assert "parsed" in resp

    # create job
    job_payload = {
        "title": "Backend Engineer",
        "description": "Looking for a Backend Engineer with Python, FastAPI and PostgreSQL. 2+ years experience"
    }
    r2 = client.post("/jobs/", json=job_payload)
    assert r2.status_code == 200
    job_id = r2.json()["job_id"]

    # match resume->job
    r3 = client.post("/match/", json={"resume_id": resume_id, "job_id": job_id})
    assert r3.status_code == 200
    resp3 = r3.json()
    assert "score" in resp3 or "results" in resp3
