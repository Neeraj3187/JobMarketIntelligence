import sqlite3
import pandas as pd

conn = sqlite3.connect("data/jobs.db")

df = pd.read_sql_query(
    "SELECT * FROM real_jobs LIMIT 10",
    conn
)

conn.close()

print(df)