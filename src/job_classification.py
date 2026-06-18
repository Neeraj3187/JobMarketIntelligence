import pandas as pd
import sqlite3

def classify_jobs():

    conn = sqlite3.connect("data/jobs.db")

    df = pd.read_sql_query(
        "SELECT * FROM real_jobs",
        conn
    )

    conn.close()

    categories = []

    for title in df["JobTitle"]:

        title = str(title).lower()

        if "ai" in title or "machine learning" in title:
            categories.append("AI/ML")

        elif "data" in title:
            categories.append("Data Science")

        elif "devops" in title or "cloud" in title:
            categories.append("DevOps")

        else:
            categories.append("Software Engineering")

    df["Category"] = categories

    return df[
        [
            "JobTitle",
            "Skills",
            "Location",
            "Company",
            "Category"
        ]
    ]