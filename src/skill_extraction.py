import sqlite3
import pandas as pd
from collections import Counter

def get_top_skills():

    conn = sqlite3.connect("data/jobs.db")

    df = pd.read_sql_query(
        "SELECT * FROM real_jobs",
        conn
    )

    conn.close()

    all_skills = []

    for skills in df["Skills"]:

        if pd.isna(skills):
            continue

        skill_list = str(skills).split(",")

        for skill in skill_list:
            all_skills.append(skill.strip())

    skill_count = Counter(all_skills)

    return skill_count