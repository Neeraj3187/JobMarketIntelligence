import sqlite3
import pandas as pd


def infer_skills(job_title):

    title = str(job_title).lower()

    skills = []

    if "python" in title:
        skills += ["Python", "SQL"]

    if "data analyst" in title:
        skills += ["Python", "SQL", "Excel", "Power BI"]

    if "data scientist" in title:
        skills += ["Python", "Machine Learning", "Pandas", "TensorFlow"]

    if "machine learning" in title or "ml" in title:
        skills += ["Python", "Machine Learning", "TensorFlow"]

    if "ai" in title:
        skills += ["Python", "LLM", "NLP"]

    if "devops" in title:
        skills += ["AWS", "Docker", "Kubernetes"]

    if "cloud" in title:
        skills += ["AWS", "Azure", "Linux"]

    if "backend" in title:
        skills += ["Python", "SQL", "APIs"]

    if "frontend" in title:
        skills += ["HTML", "CSS", "JavaScript", "React"]

    if "full stack" in title:
        skills += ["React", "Node.js", "SQL"]

    if "software engineer" in title or "developer" in title:
        skills += ["Git", "SQL", "Programming"]

    return ", ".join(list(set(skills)))


def fill_missing_skills():

    conn = sqlite3.connect("data/jobs.db")

    df = pd.read_sql(
        "SELECT * FROM real_jobs",
        conn
    )

    conn.close()

    for index, row in df.iterrows():

        if (
            pd.isna(row["Skills"])
            or str(row["Skills"]).strip() == ""
        ):
            df.at[index, "Skills"] = infer_skills(
                row["JobTitle"]
            )

    conn = sqlite3.connect("data/jobs.db")

    df.to_sql(
        "real_jobs",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Missing Skills Filled:", len(df))


if __name__ == "__main__":
    fill_missing_skills()