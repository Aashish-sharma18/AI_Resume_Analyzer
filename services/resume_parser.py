from pdfminer.high_level import extract_text
import docx

def extract_text_from_resume(path):
    if path.endswith(".pdf"):
        return extract_text(path)

    elif path.endswith(".docx"):
        doc = docx.Document(path)
        return " ".join([p.text for p in doc.paragraphs])

    else:
        return ""
