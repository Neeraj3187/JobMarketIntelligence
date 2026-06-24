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
        
        st.progress(80)

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

    missing_skills = jd_missing_skills

    score = calculate_resume_score(
        resume_text,
        missing_skills
    )

    st.subheader("ATS Score")

    ats_score = score

    st.metric(
        "ATS Compatibility",
        f"{ats_score}/100"
    )

    if ats_score >= 80:
        st.success("Excellent ATS Compatibility")

    elif ats_score >= 60:
        st.warning("Good ATS Compatibility")

    else:
        st.error("Low ATS Compatibility")

    st.subheader("Resume Strengths")

    strengths = []

    resume_lower = resume_text.lower()

    for skill in [
        "python",
        "sql",
        "git",
        "aws",
        "docker",
        "machine learning"
    ]:
        if skill in resume_lower:
            strengths.append(skill.upper())

    if strengths:

        for skill in strengths:
            st.markdown(f"- ✅ **{skill}**")

    else:
        st.warning(
            "No major strengths detected"
        )

    st.subheader("Skill Gap Analysis")

    matched_skills = len(strengths)
    missing_count = len(missing_skills)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Matched Skills",
            matched_skills
        )

    with col2:
        st.metric(
            "Missing Skills",
            missing_count
        )
    chart_df = pd.DataFrame(
        {
            "Count": [
                matched_skills,
                missing_count
            ]
        },
        index=[
            "Matched Skills",
            "Missing Skills"
        ]
    )

    st.bar_chart(chart_df)

    st.subheader("Resume Score")

    if score >= 90:
        st.success(f"🟢 Resume Score: {score}")

    elif score >= 70:
        st.warning(f"🟡 Resume Score: {score}")

    else:
        st.error(f"🔴 Resume Score: {score}")
    st.subheader("Download Report")

    if st.button("Generate PDF Report"):

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
                label="⬇️ Download PDF",
                data=pdf_file,
                file_name="resume_report.pdf",
                mime="application/pdf"
            )
