ATS_KEYWORDS = [
    "experience", "skills", "projects",
    "education", "certifications", "summary"
]

def ats_score(resume_text):
    found = sum(1 for k in ATS_KEYWORDS if k in resume_text.lower())
    return round((found / len(ATS_KEYWORDS)) * 100, 2)
