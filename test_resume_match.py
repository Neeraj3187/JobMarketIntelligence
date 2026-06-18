import sqlite3
import pandas as pd

from src.resume_matcher import calculate_similarity

resume_text = """
HTML
CSS
JavaScript
C++
Computer Science
"""

conn = sqlite3.connect("data/jobs.db")

jobs_df = pd.read_sql(
    "SELECT * FROM real_jobs",
    conn
)

conn.close()

similarities = calculate_similarity(
    resume_text,
    jobs_df
)

jobs_df["MatchScore"] = similarities * 100

top_jobs = jobs_df.sort_values(
    by="MatchScore",
    ascending=False
).head(10)

print(
    top_jobs[
        ["JobTitle", "Company", "MatchScore"]
    ]
)