from app.services.parser import extract_email, extract_phone, extract_skills, estimate_experience_years, extract_title

def test_email_phone_skills_exp():
    sample = """
    John Doe
    Software Engineer
    john.doe@example.com
    +91 9876543210
    Experience: 3+ years working with Python, FastAPI, PostgreSQL, Docker
    """
    assert extract_email(sample) == "john.doe@example.com"
    assert "9876543210" in extract_phone(sample).replace(" ", "")
    skills = extract_skills(sample)
    assert "python" in skills
    assert "fastapi" in skills or "fastapi" in " ".join(skills)
    assert estimate_experience_years(sample) == 3
    title = extract_title(sample)
    assert "Software" in title

def test_empty_text():
    assert extract_email("") is None
    assert extract_phone("") is None
    assert extract_skills("") == []
    assert estimate_experience_years("") is None