import streamlit as st
import sqlite3
import pandas as pd

from src.job_classification import classify_jobs
from src.skill_extraction import get_top_skills
from src.location_analysis import get_top_locations

st.set_page_config(
    page_title="Job Market Intelligence",
    layout="wide"
)

st.title("🚀 Job Market Intelligence Dashboard")

# Database Stats
conn = sqlite3.connect("data/jobs.db")
df = pd.read_sql("SELECT * FROM real_jobs", conn)
conn.close()

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Jobs", len(df))

with col2:
    st.metric("IT Jobs", 320)

# Categories
st.subheader("Job Categories")

cat_df = classify_jobs()

st.bar_chart(
    cat_df["Category"].value_counts()
)

# Skills
st.subheader("Top Skills")

skills = get_top_skills().most_common(10)

skill_df = pd.DataFrame(
    skills,
    columns=["Skill", "Count"]
)

st.bar_chart(
    skill_df.set_index("Skill")
)

# Locations
st.subheader("Top Locations")

locs = get_top_locations().most_common(10)

loc_df = pd.DataFrame(
    locs,
    columns=["Location", "Count"]
)

st.bar_chart(
    loc_df.set_index("Location")
)

st.success("Job Market Intelligence System Running")
st.header("Resume Matcher")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
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
    similarities = calculate_similarity(
    resume_text,
    df
)

df["MatchScore"] = similarities * 100

top_jobs = df.sort_values(
    "MatchScore",
    ascending=False
).head(10)

st.subheader("Top Matching Jobs")

st.dataframe(
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

st.subheader("Missing Skills")

if missing_skills:
    st.write(missing_skills)
else:
    st.success("No Missing Skills Found")