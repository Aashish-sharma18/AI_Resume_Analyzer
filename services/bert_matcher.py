from sklearn.metrics.pairwise import cosine_similarity
from models.bert_model import get_embedding

def bert_match(resume_text, job_text):
    resume_vec = get_embedding(resume_text)
    job_vec = get_embedding(job_text)

    similarity = cosine_similarity([resume_vec], [job_vec])
    return round(similarity[0][0] * 100, 2)
