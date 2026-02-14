def final_score(skill_match_percent, bert_score):
    score = (0.4 * skill_match_percent) + (0.6 * bert_score)
    return round(min(score, 100), 2)
