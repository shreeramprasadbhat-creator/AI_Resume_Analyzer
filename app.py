import streamlit as st

from utils import (
    extract_text_from_pdf,
    detect_skills,
    calculate_resume_score,
    analyze_resume
)

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get AI-powered feedback.")

uploaded_file = st.file_uploader(
    "Choose your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("✅ Resume uploaded successfully!")

    resume_text = extract_text_from_pdf(uploaded_file)

    skills = detect_skills(resume_text)

    score = calculate_resume_score(resume_text, skills)

    st.subheader("📄 Resume Text")

    st.text_area(
        "Extracted Resume",
        resume_text,
        height=250
    )

    st.subheader("🛠 Detected Skills")

    if skills:
        for skill in skills:
            st.success(skill)
    else:
        st.warning("No skills detected.")

    st.subheader("📊 Resume Score")

    st.progress(score / 100)

    st.success(f"Resume Score: {score}/100")

    with st.spinner("🤖 Gemini is analyzing your resume..."):
        analysis = analyze_resume(resume_text, skills)

    st.subheader("🤖 AI Resume Analysis")

    st.markdown(analysis)