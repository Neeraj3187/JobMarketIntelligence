import sqlite3
import pandas as pd
from collections import Counter

def get_top_locations():

    conn = sqlite3.connect("data/jobs.db")

    df = pd.read_sql_query(
        "SELECT * FROM real_jobs",
        conn
    )

    conn.close()

    location_count = Counter(df["Location"])

    return location_count