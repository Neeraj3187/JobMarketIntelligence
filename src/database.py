import sqlite3
import pandas as pd

def create_database():

    conn = sqlite3.connect("data/jobs.db")

    df = pd.read_csv("data/jobs.csv")

    df.to_sql(
        "jobs",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Database Created Successfully")