import requests
import pandas as pd
import sqlite3

url = "https://remoteok.com/api"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    print("Fetching jobs from API...")

    response = requests.get(
        url,
        headers=headers,
        timeout=60
    )

    print("API Response:", response.status_code)

    data = response.json()

    print("Total API Jobs:", len(data) - 1)

except Exception as e:

    print("API Error:", e)
    exit()

it_keywords = [
    "python",
    "developer",
    "software",
    "engineer",
    "data",
    "ai",
    "machine learning",
    "devops",
    "cloud",
    "backend",
    "frontend",
    "full stack",
    "java",
    "javascript",
    "react",
    "node",
    "aws",
    "cybersecurity",
    "sql",
    "analytics",
    "analyst",
    "ml",
    "deep learning",
    "docker",
    "kubernetes",
    "linux",
    "security",
    "web",
    "api",
    "database",
    "programmer",
    "technology",
    "engineering",
    "qa",
    "testing",
    "sre",
    "product",
    "technical",
    "automation",
    "systems",
    "network",
    "support",
    "it"
]

valid_skills = [
    "python",
    "sql",
    "aws",
    "docker",
    "kubernetes",
    "linux",
    "java",
    "javascript",
    "react",
    "node",
    "machine learning",
    "data science",
    "tensorflow",
    "pytorch",
    "devops",
    "cloud",
    "cybersecurity",
    "mongodb",
    "mysql",
    "postgresql",
    "git",
    "github",
    "jira"
]

jobs = []

for job in data[1:]:

    title = str(job.get("position", "")).lower()
    tags = " ".join(job.get("tags", [])).lower()

    if (
        any(keyword in title for keyword in it_keywords)
        or
        any(keyword in tags for keyword in it_keywords)
    ):

        filtered_skills = []

        for tag in job.get("tags", []):

            if tag.lower() in valid_skills:
                filtered_skills.append(tag)

        jobs.append({
            "JobTitle": job.get("position", ""),
            "Company": job.get("company", ""),
            "Location": job.get("location", ""),
            "Skills": ", ".join(filtered_skills),
            "JobLink": job.get("apply_url", "")
        })

df = pd.DataFrame(jobs)

conn = sqlite3.connect("data/jobs.db")

df.to_sql(
    "real_jobs",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("IT Jobs Saved:", len(df))
print("Database Updated Successfully")