
from typing import Dict

IN_MEMORY_DB = {
    "resumes": {},  # resume_id -> {filename, text, parsed}
    "jobs": {}      # job_id -> {title, jd_text, parsed}
}
