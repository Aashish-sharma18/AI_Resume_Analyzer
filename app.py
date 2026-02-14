from flask import Flask, render_template, request, redirect, url_for, session
import os
import pandas as pd

# ================= CONFIG =================
from config import (
    UPLOAD_FOLDER,
    ALLOWED_EXTENSIONS,
    DEBUG,
    HOST,
    PORT,
    SECRET_KEY
)

# ================= SERVICES =================
from services.resume_parser import extract_text_from_resume
from services.skill_extractor import extract_skills, missing_skills
from services.bert_matcher import bert_match
from services.scorer import final_score
from services.ats_checker import ats_score
from services.resume_suggestions import suggestions

# ================= AUTH =================
from auth import register, login

# ================= APP INIT =================
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= LOAD JOB DATA =================
jobs = pd.read_csv("data/job_descriptions.csv")

# ================= HELPERS =================
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ================= AUTH ROUTES =================
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if login(username, password):
            session["user"] = username
            return redirect(url_for("index"))
        return "Invalid credentials"

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if register(username, password):
            return redirect(url_for("login_page"))
        return "User already exists"

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page"))

# ================= MAIN ROUTE =================
@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login_page"))

    if request.method == "POST":

        # ---------- FILE VALIDATION ----------
        if "resume" not in request.files:
            return redirect(request.url)

        file = request.files["resume"]

        if file.filename == "":
            return redirect(request.url)

        if not allowed_file(file.filename):
            return "Only PDF and DOCX files are allowed"

        # ---------- JOB SELECTION ----------
        job_index = int(request.form["job"])
        job_text = jobs.iloc[job_index]["description"]

        # ---------- SAVE FILE ----------
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # ---------- EXTRACT TEXT ----------
        resume_text = extract_text_from_resume(filepath)

        # ---------- SKILLS ----------
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_text)

        skill_match_percent = (
            len(set(resume_skills) & set(job_skills)) / max(len(job_skills), 1)
        ) * 100

        # ---------- BERT MATCH ----------
        bert_score = bert_match(resume_text, job_text)

        # ---------- FINAL SCORE ----------
        score = final_score(skill_match_percent, bert_score)

        # ---------- SKILL GAP ----------
        missing = missing_skills(resume_skills, job_skills)

        # ---------- ATS SCORE ----------
        ats = ats_score(resume_text)

        # ---------- AI SUGGESTIONS ----------
        tips = suggestions(missing)

        return render_template(
            "dashboard.html",
            skill_match=round(skill_match_percent, 2),
            bert_score=bert_score,
            final_score=score,
            ats_score=ats,
            matched=resume_skills,
            missing=missing,
            tips=tips,
            username=session["user"]
        )

    return render_template("index.html", jobs=jobs, username=session["user"])

# ================= RUN SERVER =================
if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)
