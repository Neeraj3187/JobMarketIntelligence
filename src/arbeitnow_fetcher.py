import requests
import pandas as pd


def fetch_arbeitnow_jobs():

    url = "https://www.arbeitnow.com/api/job-board-api"

    try:

        response = requests.get(
            url,
            timeout=30
        )

        data = response.json()

        jobs = []

        for job in data["data"]:

            jobs.append({
                "JobTitle": job.get("title", ""),
                "Company": job.get("company_name", ""),
                "Location": job.get("location", ""),
                "Skills": ", ".join(job.get("tags", [])),
                "JobLink": job.get("url", ""),
                "Source": "Arbeitnow"
            })

        return pd.DataFrame(jobs)

    except Exception as e:

        print("Arbeitnow Error:", e)

        return pd.DataFrame()