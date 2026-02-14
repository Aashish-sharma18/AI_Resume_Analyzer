import pandas as pd

skills = pd.read_csv("data/skills.csv", header=None)[0].tolist()

def extract_skills(text):
    text = text.lower()
    found = [skill for skill in skills if skill.lower() in text]
    return list(set(found))

def missing_skills(resume_skills, job_skills):
    return list(set(job_skills) - set(resume_skills))

