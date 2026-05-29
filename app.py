from flask import Flask, render_template, request
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)

# --------------------------
# Skills Database
# --------------------------

skills_db = [
    "python",
    "machine learning",
    "deep learning",
    "sql",
    "tensorflow",
    "nlp",
    "data analysis"
]

# --------------------------
# Extract Text
# --------------------------

def extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            if page.extract_text():

                text += page.extract_text()

    return text

# --------------------------
# Extract Skills
# --------------------------

def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in skills_db:

        if skill in text:

            found_skills.append(skill)

    return found_skills

# --------------------------
# ATS Score
# --------------------------

def ats_score(skills):

    score = (len(skills) / len(skills_db)) * 100

    return round(score, 2)

# --------------------------
# Job Match %
# --------------------------

def match_percentage(resume, jd):

    text = [resume, jd]

    cv = CountVectorizer()

    matrix = cv.fit_transform(text)

    similarity = (
        matrix * matrix.T
    ).toarray()[0][1]

    return round(similarity * 100, 2)

# --------------------------
# Flask Routes
# --------------------------

@app.route("/", methods=["GET", "POST"])

def home():

    if request.method == "POST":

        uploaded_file = request.files["resume"]

        jd = request.form["jd"]

        resume_text = extract_text(uploaded_file)

        skills = extract_skills(resume_text)

        score = ats_score(skills)

        match = match_percentage(
            resume_text,
            jd
        )

        return render_template(
            "index.html",
            skills=skills,
            score=score,
            match=match
        )

    return render_template("index.html")

# --------------------------
# Run App
# --------------------------

if __name__ == "__main__":

    app.run(debug=True)