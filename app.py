import streamlit as st
import pdfplumber
import docx
import re
from collections import Counter

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- TITLE ---------------- #
st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and get ATS score, skills analysis, and role recommendations.")

# ---------------- SKILLS DATABASE ---------------- #
SKILLS_DB = {
    "Python": ["python", "numpy", "pandas", "matplotlib"],
    "Machine Learning": ["machine learning", "sklearn", "scikit-learn"],
    "Deep Learning": ["tensorflow", "keras", "pytorch"],
    "Data Analysis": ["excel", "power bi", "tableau", "sql"],
    "Web Development": ["html", "css", "javascript", "flask", "streamlit"],
    "Cloud": ["aws", "azure", "gcp"],
    "Database": ["mysql", "mongodb", "postgresql"],
}

ROLE_RECOMMENDATIONS = {
    "Python": "Python Developer",
    "Machine Learning": "ML Engineer",
    "Deep Learning": "AI Engineer",
    "Data Analysis": "Data Analyst",
    "Web Development": "Full Stack Developer",
    "Cloud": "Cloud Engineer",
    "Database": "Database Administrator"
}

# ---------------- FILE TEXT EXTRACTION ---------------- #
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    elif uploaded_file.name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)

    elif uploaded_file.name.endswith(".txt"):
        return str(uploaded_file.read(), "utf-8")

    return ""

# ---------------- SKILL EXTRACTION ---------------- #
def extract_skills(text):
    found_skills = []

    text = text.lower()

    for category, skills in SKILLS_DB.items():
        for skill in skills:
            if skill.lower() in text:
                found_skills.append(category)

    return list(set(found_skills))

# ---------------- ATS SCORE ---------------- #
def calculate_ats_score(text):
    score = 0

    keywords = [
        "python",
        "machine learning",
        "deep learning",
        "projects",
        "experience",
        "skills",
        "education",
        "tensorflow",
        "sql",
        "data"
    ]

    text = text.lower()

    for keyword in keywords:
        if keyword in text:
            score += 10

    return min(score, 100)

# ---------------- RESUME SECTION DETECTION ---------------- #
def detect_sections(text):
    sections = []

    possible_sections = [
        "education",
        "skills",
        "projects",
        "experience",
        "certifications",
        "internship",
        "achievements"
    ]

    text = text.lower()

    for sec in possible_sections:
        if sec in text:
            sections.append(sec.title())

    return sections

# ---------------- FILE UPLOADER ---------------- #
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

# ---------------- PROCESS FILE ---------------- #
if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    text = extract_text(uploaded_file)

    # ---------- Resume Preview ---------- #
    with st.expander("📃 Resume Preview"):
        st.text(text[:5000])

    # ---------- ATS Score ---------- #
    ats_score = calculate_ats_score(text)

    st.subheader("📊 ATS Score")

    st.progress(ats_score / 100)

    st.metric("ATS Score", f"{ats_score}/100")

    # ---------- Skills ---------- #
    skills = extract_skills(text)

    st.subheader("🛠 Detected Skills")

    if skills:
        for skill in skills:
            st.success(skill)
    else:
        st.warning("No major skills detected.")

    # ---------- Sections ---------- #
    sections = detect_sections(text)

    st.subheader("📂 Resume Sections Found")

    if sections:
        st.write(sections)
    else:
        st.warning("Important resume sections missing.")

    # ---------- Role Recommendation ---------- #
    st.subheader("💼 Recommended Roles")

    recommended_roles = []

    for skill in skills:
        if skill in ROLE_RECOMMENDATIONS:
            recommended_roles.append(
                ROLE_RECOMMENDATIONS[skill]
            )

    recommended_roles = list(set(recommended_roles))

    if recommended_roles:
        for role in recommended_roles:
            st.info(role)
    else:
        st.warning("No role recommendations available.")

    # ---------- Word Count ---------- #
    word_count = len(text.split())

    st.subheader("📝 Resume Statistics")

    col1, col2 = st.columns(2)

    col1.metric("Total Words", word_count)
    col2.metric("Detected Skills", len(skills))

    # ---------- Suggestions ---------- #
    st.subheader("🚀 Resume Improvement Suggestions")

    suggestions = []

    if ats_score < 60:
        suggestions.append("Add more technical keywords.")

    if "Projects" not in sections:
        suggestions.append("Add a Projects section.")

    if "Skills" not in sections:
        suggestions.append("Add a Skills section.")

    if word_count < 300:
        suggestions.append("Resume content is too short.")

    if suggestions:
        for s in suggestions:
            st.warning(s)
    else:
        st.success("Your resume looks strong!")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("Built with Streamlit + Python")