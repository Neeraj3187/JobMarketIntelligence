import streamlit as st
import sqlite3
import pandas as pd

from src.job_classification import classify_jobs
from src.skill_extraction import get_top_skills
from src.location_analysis import get_top_locations
from src.pdf_reader import extract_text_from_pdf
from src.resume_matcher import (
    recommend_career,
    calculate_similarity,
    calculate_resume_score,
    get_missing_skills,
    calculate_jd_match,
    get_jd_missing_skills,
    get_resume_feedback
)
from src.pdf_report import generate_report

st.set_page_config(
    page_title="Job Market Intelligence",
    layout="wide"
)

st.title("Job Market Intelligence Dashboard")

conn = sqlite3.connect("data/jobs.db")
df = pd.read_sql("SELECT * FROM real_jobs", conn)
conn.close()

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Jobs", len(df))

with col2:
    st.metric("IT Jobs", 320)

st.subheader("Job Categories")
cat_df = classify_jobs()
st.bar_chart(cat_df["Category"].value_counts())

st.subheader("Top Skills")
skills = get_top_skills().most_common(10)
skill_df = pd.DataFrame(skills, columns=["Skill", "Count"])
st.bar_chart(skill_df.set_index("Skill"))

st.subheader("Top Locations")
locs = get_top_locations().most_common(10)
loc_df = pd.DataFrame(locs, columns=["Location", "Count"])
st.bar_chart(loc_df.set_index("Location"))

st.success("Job Market Intelligence System Running")
st.header("Resume Matcher")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)
job_description = st.text_area(
    "Paste Job Description",
    height=200
)

if uploaded_file is not None:

    resume_text = extract_text_from_pdf(
        uploaded_file
    )

    career = recommend_career(
        resume_text
    )

    st.subheader(
        "Career Recommendation"
    )

    st.write(career)
    if job_description.strip():

        jd_score = calculate_jd_match(
            resume_text,
            job_description
        )

        st.subheader("Resume vs JD Match")

        st.metric(
            "Match %",
            f"{jd_score:.2f}%"
        )
        jd_missing_skills = get_jd_missing_skills(
            resume_text,
            job_description
        )

        st.subheader("JD Missing Skills")

        if jd_missing_skills:

            for skill in jd_missing_skills:
                st.write(f"❌ {skill}")

        else:
            st.success(
                "No JD Skills Missing"
            )
    similarities = calculate_similarity(
        resume_text,
        df
    )

    df["MatchScore"] = (similarities * 100).round(2)

    top_jobs = df.sort_values(
        "MatchScore",
        ascending=False
    ).head(10)

    st.subheader("Top Matching Jobs")
    

    st.table(
    top_jobs[
        [
            "JobTitle",
            "Company",
            "Location",
            "MatchScore"
        ]
    ]
)

    missing_skills = get_missing_skills(
        resume_text,
        "python, sql, aws, docker, kubernetes"
    )

    score = calculate_resume_score(
        resume_text,
        missing_skills
    )

    st.subheader("Resume Score")
    st.metric("Score", score)

    feedback = get_resume_feedback(
        score
    )

    st.subheader(
        "Resume Feedback"
    )

    st.success(
        feedback
    )

    st.subheader("Missing Skills")
    if missing_skills:
        st.write(missing_skills)
    else:
        st.success("No Missing Skills Found")

    st.subheader("AI Learning Roadmap")

    if missing_skills:

        st.write("To improve your resume score, learn:")

        for skill in missing_skills:
            st.write(f"✅ {skill}")

        predicted_score = min(
            score + (len(missing_skills) * 10),
            100
        )

        st.metric(
            "Predicted Score After Learning",
            predicted_score
        )
        generate_report(
            "resume_report.pdf",
            career,
            score,
            missing_skills,
            top_jobs
        )

        with open(
            "resume_report.pdf",
            "rb"
        ) as pdf_file:

            st.download_button(
                label="📄 Download Resume Report",
                data=pdf_file,
                file_name="resume_report.pdf",
                mime="application/pdf"
            )
