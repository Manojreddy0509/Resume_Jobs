import re
from difflib import SequenceMatcher

COMMON_SKILLS = [
    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "go", "rust", "scala", "kotlin", "swift", "r",

    # Web / Backend Frameworks
    "fastapi", "flask", "django", "spring", "spring boot",
    "node", "node.js", "express", "nestjs",

    # Frontend
    "react", "angular", "vue", "next.js", "html", "css",
    "tailwind", "bootstrap",

    # Databases
    "sql", "mysql", "postgresql", "postgres", "sqlite",
    "mongodb", "redis", "cassandra", "elasticsearch",

    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes",
    "terraform", "jenkins", "github actions", "ci/cd",

    # Data / ML / AI
    "machine learning", "deep learning", "ml", "dl",
    "nlp", "computer vision", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch",

    # Data Engineering
    "spark", "hadoop", "kafka", "airflow",

    # Tools & Misc
    "git", "linux", "bash", "rest api", "graphql",
    "microservices", "system design"
]

# synonym map for quick normalization
SYNONYMS = {
    "node": ["node.js", "nodejs"],
    "postgresql": ["postgres"],
    "tensorflow": ["tf"],
    "pytorch": ["torch"],
    "javascript": ["js"],
    "typescript": ["ts"],
    "machine learning": ["ml"],
}

def normalize_skill(found: str):
    f = found.lower().strip()
    # map synonyms to canonical
    for canon, syns in SYNONYMS.items():
        if f == canon or f in syns:
            return canon
    return f

def extract_email(text: str):
    if not text:
        return None
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group() if match else None

def extract_phone(text: str):
    if not text:
        return None
    # Accept formats like +91-9876543210, 9876543210, (123) 456-7890
    # This is permissive; further normalization is possible
    match = re.search(r"(\+?\d{1,3}[\s\-\.]?)?(\(?\d{2,4}\)?[\s\-\.]?)?\d{6,12}", text)
    return match.group().strip() if match else None

def extract_skills(text: str):
    if not text:
        return []
    text_lower = text.lower()
    found = set()
    # exact substring match for each known skill
    for skill in COMMON_SKILLS:
        if skill in text_lower:
            found.add(normalize_skill(skill))
    # also try token-level find (catch 'JS' or 'tf' etc.)
    tokens = re.findall(r"[A-Za-z#+\-\.\#]+", text_lower)
    for t in tokens:
        t = t.strip()
        # avoid single chars
        if len(t) <= 1:
            continue
        # check mapping for synonyms
        for canon, syns in SYNONYMS.items():
            if t == canon or t in syns:
                found.add(canon)
        if t in COMMON_SKILLS:
            found.add(normalize_skill(t))
    return sorted(list(found))

def estimate_experience_years(text: str):
    if not text:
        return None
    # Look for "X years" or "X+ years" or ranges "2-4 years" or duration "2019 - 2022"
    text_lower = text.lower()
    # First try explicit "X years"
    m = re.findall(r"(\d+)\s*\+?\s*years?", text_lower)
    if m:
        years = [int(x) for x in m]
        return max(years)
    # ranges like "2-4 years"
    m2 = re.findall(r"(\d+)\s*-\s*(\d+)\s*years?", text_lower)
    if m2:
        pairs = [(int(a), int(b)) for a,b in m2]
        # take max upper bound
        return max(b for a,b in pairs)
    # try infer from dates like "2019 - 2022"
    years_dates = re.findall(r"(20\d{2}|19\d{2})", text_lower)
    if len(years_dates) >= 2:
        ints = [int(x) for x in years_dates]
        return max(ints) - min(ints)
    return None

def extract_title(text: str):
    """
    Heuristic: first non-empty line with <= 6 words and containing keywords like 'engineer', 'developer', 'manager'
    """
    if not text:
        return None
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    keywords = ["engineer", "developer", "data", "scientist", "manager", "intern", "analyst", "lead", "software", "backend", "frontend", "full stack", "sde"]
    for line in lines[:6]:
        low = line.lower()
        if any(k in low for k in keywords) and len(line.split()) <= 8:
            return line
    # fallback: first non-empty line
    return lines[0] if lines else None

def title_similarity(a: str, b: str):
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()