import os

# ===============================
# BASE DIRECTORY
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===============================
# UPLOAD CONFIGURATION
# ===============================
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_FILE_SIZE_MB = 5

# ===============================
# DATA PATHS
# ===============================
DATA_DIR = os.path.join(BASE_DIR, "data")
SKILLS_FILE = os.path.join(DATA_DIR, "skills.csv")
JOB_DESC_FILE = os.path.join(DATA_DIR, "job_descriptions.csv")

# ===============================
# NLP / ML CONFIG
# ===============================
BERT_MODEL_NAME = "all-MiniLM-L6-v2"
SKILL_MATCH_WEIGHT = 0.4
BERT_MATCH_WEIGHT = 0.6

# ===============================
# FLASK CONFIG
# ===============================
DEBUG = True
SECRET_KEY = "resume-analyzer-secret-key"

# ===============================
# DEPLOYMENT CONFIG
# ===============================
HOST = "0.0.0.0"
PORT = 5000
