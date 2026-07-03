import os
from dotenv import load_dotenv
import pdfplumber
import google.generativeai as genai

print(">>> utils.py loaded <<<")

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def extract_text_from_pdf(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def detect_skills(text):
    skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Matplotlib",
        "Seaborn",
        "Git",
        "GitHub",
        "Streamlit",
        "Flask",
        "Docker"
    ]

    found = []

    for skill in skills:
        if skill.lower() in text.lower():
            found.append(skill)

    return found


def calculate_resume_score(text, skills):
    score = 0

    score += min(len(skills) * 5, 40)

    if any(word.lower() in text.lower() for word in
           ["b.tech", "bachelor", "engineering", "degree", "m.tech"]):
        score += 20

    if any(word.lower() in text.lower() for word in
           ["project", "developed", "built", "created"]):
        score += 20

    if any(word.lower() in text.lower() for word in
           ["internship", "experience", "worked"]):
        score += 20

    return min(score, 100)


def analyze_resume(text, skills):
    prompt = f"""
You are an expert HR recruiter.

Analyze this resume.

Resume:
{text}

Detected Skills:
{', '.join(skills)}

Return the response in Markdown.

# Overall Score
Give score out of 100.

# Strengths
- ...

# Weaknesses
- ...

# Suggestions
- ...

# Suitable Roles
- ...

# Missing Skills
- ...
"""

    try:
        response = model.generate_content(prompt)

        print("========== GEMINI RESPONSE ==========")
        print(response.text)
        print("=====================================")

        return response.text

    except Exception as e:
        return f"Gemini Error: {e}"