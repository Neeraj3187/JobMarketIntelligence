import sqlite3
import pandas as pd

from src.arbeitnow_fetcher import fetch_arbeitnow_jobs
from src.jsearch_fetcher import fetch_jsearch_jobs

conn = sqlite3.connect("data/jobs.db")

remote_df = pd.read_sql(
    "SELECT * FROM real_jobs",
    conn
)

conn.close()

arbeit_df = fetch_arbeitnow_jobs()

jsearch_df = fetch_jsearch_jobs()

all_jobs = pd.concat(
    [remote_df, arbeit_df, jsearch_df],
    ignore_index=True
)

all_jobs.drop_duplicates(
    subset=["JobTitle", "Company"],
    inplace=True
)

conn = sqlite3.connect("data/jobs.db")

all_jobs.to_sql(
    "real_jobs",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Total Jobs Saved:", len(all_jobs))