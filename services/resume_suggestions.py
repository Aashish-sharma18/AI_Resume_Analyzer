def suggestions(missing_skills):
    tips = []
    for skill in missing_skills:
        tips.append(f"Consider adding projects or experience related to {skill}")
    return tips
